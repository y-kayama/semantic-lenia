import os
import random
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def set_deterministic_environment(seed: int = 42) -> None:
    """
    Configure a controlled pseudo-random environment for trajectory-level comparison.

    This improves repeatability within a matched software/hardware stack, but it does
    not guarantee bitwise-identical generation across different GPU architectures.
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class UnifiedSemanticLeniaPhase1:
    """
    Macroscopic logit-level Semantic Lenia engine.

    State used for U_t
    ------------------
    c_t is the normalized hidden state from the final Transformer layer at the
    current final sequence position:
        outputs.hidden_states[-1][:, -1, :]

    Target centroid
    ---------------
    For compatibility with the published experiments, each target concept string is
    tokenized with a leading space and the output-embedding vector of its first token
    is used. The centroid is the normalized mean of those vectors.

    Token-level PPL signal
    ----------------------
    ppl_t is exp(-log p(w_t)) = 1 / p(w_t), where w_t is the sampled token and p(w_t)
    is measured from the temperature-scaled, already-steered next-token distribution.
    It is therefore an instantaneous sampled-token inverse probability, not standard
    sequence perplexity computed from mean NLL over a corpus.
    """

    def __init__(self, model_name: str, use_4bit: bool = False):
        print(
            f"Loading Semantic Lenia substrate: {model_name} "
            f"(4bit_quantization={use_4bit})..."
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto",
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
            )

        self.model.eval()
        self.vocab_embeddings = F.normalize(
            self.model.get_output_embeddings().weight.detach().to(torch.float16),
            p=2,
            dim=-1,
        )

    def _get_target_centroid(self, target_concepts: List[str]) -> torch.Tensor:
        vectors = []
        for concept in target_concepts:
            ids = self.tokenizer(
                " " + concept, add_special_tokens=False
            ).input_ids
            if ids:
                vectors.append(self.vocab_embeddings[ids[0]])

        if not vectors:
            raise ValueError("No valid target-concept token vectors were produced.")

        centroid = torch.stack(vectors).mean(dim=0)
        return F.normalize(centroid, p=2, dim=0).unsqueeze(0)

    @staticmethod
    def _growth(u_val: float, mu: float, sigma: float) -> float:
        if sigma <= 0:
            raise ValueError("sigma must be > 0.")

        diff = u_val - mu
        exponent = -0.5 * (diff / sigma) ** 2
        g_u_val = 2.0 * np.exp(exponent) - 1.0

        # Asymmetric dead-zone cutoff.
        delta_width = sigma * np.sqrt(2.0 * np.log(2.0))
        if u_val < (mu - delta_width):
            g_u_val = 0.0

        return float(g_u_val)

    def generate(
        self,
        prompt: str,
        target_concepts: List[str],
        mode: str = "wild",
        mu: float = 0.5,
        sigma: float = 0.1,
        alpha: float = 30.0,
        max_new_tokens: int = 80,
        temperature: float = 0.8,
        record_hidden_states: bool = False,
    ) -> Tuple[str, List[Dict]]:
        if temperature <= 0:
            raise ValueError("temperature must be > 0.")

        initial_device = self.model.device
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(
            initial_device
        )
        generated_ids = input_ids

        k_kernel = self._get_target_centroid(target_concepts)
        vocab_sim_to_k = torch.matmul(
            k_kernel, self.vocab_embeddings.t()
        ).squeeze(0)

        trajectory_log: List[Dict] = []
        past_key_values = None
        current_input = input_ids

        for step in range(max_new_tokens):
            with torch.no_grad():
                outputs = self.model(
                    current_input,
                    past_key_values=past_key_values,
                    output_hidden_states=True,
                    use_cache=True,
                )
                past_key_values = outputs.past_key_values

                logits = outputs.logits[:, -1, :]
                current_device = logits.device

                # c_t: final-layer hidden state at the current final sequence position.
                c_t = F.normalize(
                    outputs.hidden_states[-1][:, -1, :], p=2, dim=-1
                )

                k_kernel_local = k_kernel.to(current_device)
                vocab_sim_local = vocab_sim_to_k.to(current_device)

                u_raw = torch.matmul(c_t, k_kernel_local.t())
                u_val = ((u_raw + 1.0) / 2.0).item()
                g_u_val = self._growth(u_val, mu, sigma)

                g_u = torch.tensor(
                    g_u_val, dtype=logits.dtype, device=current_device
                )

                if mode == "wild":
                    logits[0] += alpha * g_u * vocab_sim_local
                elif mode not in {"baseline", "none"}:
                    raise ValueError(
                        f"Unknown mode={mode!r}; use 'wild', 'baseline', or 'none'."
                    )

                probs = F.softmax(logits / temperature, dim=-1)
                next_token = torch.multinomial(probs, 1)

                current_input = next_token.to(initial_device)
                generated_ids = torch.cat(
                    [generated_ids, next_token.to(initial_device)], dim=-1
                )

                token_prob = probs[0, next_token.item()].item()
                sampled_token_ppl = 1.0 / max(token_prob, 1e-10)

                item: Dict = {
                    "step": step,
                    "u_potential": round(u_val, 6),
                    "g_growth": round(g_u_val, 6),
                    # Backward-compatible key used by existing analysis files.
                    "ppl_t": float(sampled_token_ppl),
                    # Explicit name documenting what ppl_t actually measures.
                    "sampled_token_ppl": float(sampled_token_ppl),
                    "token_probability": float(token_prob),
                    "token": self.tokenizer.decode(next_token.item()),
                }

                if record_hidden_states:
                    item["hidden_state"] = (
                        c_t.detach().to("cpu", dtype=torch.float32)
                        .numpy()
                        .reshape(-1)
                        .tolist()
                    )

                trajectory_log.append(item)

                if next_token.item() == self.tokenizer.eos_token_id:
                    break

        full_text = self.tokenizer.decode(
            generated_ids[0], skip_special_tokens=True
        )
        return full_text, trajectory_log

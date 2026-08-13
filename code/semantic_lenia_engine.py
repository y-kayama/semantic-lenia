import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import numpy as np
import random
import os
from typing import List, Tuple, Dict

def set_deterministic_environment(seed=42):
    """Ensure strict deterministic execution for dynamical system reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed) 
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

class UnifiedSemanticLeniaPhase1:
    """
    Phase 1: Macroscopic Logit-Level Semantic Lenia Engine
    Includes optimized KV-caching and Multi-GPU dynamic tensor alignment.
    """
    def __init__(self, model_name: str, use_4bit: bool = False):
        print(f"Loading Unified Lenia Substrate: {model_name} (4bit_quantization={use_4bit})...")
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
                device_map="auto" 
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, 
                torch_dtype=torch.float16, 
                device_map="auto"
            )
        self.model.eval()

        # Maintain vocabulary embeddings in float16 for cross-device compatibility
        self.vocab_embeddings = F.normalize(
            self.model.get_output_embeddings().weight.detach().to(torch.float16), 
            p=2, dim=-1
        )

    def _get_target_centroid(self, target_concepts: List[str]) -> torch.Tensor:
        vectors = []
        for word in target_concepts:
            ids = self.tokenizer(" " + word, add_special_tokens=False).input_ids
            if ids:
                vectors.append(self.vocab_embeddings[ids[0]])
        centroid = torch.stack(vectors).mean(dim=0)
        return F.normalize(centroid, p=2, dim=0).unsqueeze(0)

    def generate(self, 
                 prompt: str, 
                 target_concepts: List[str], 
                 mode: str = "wild", 
                 mu: float = 0.5,     
                 sigma: float = 0.1,  
                 alpha: float = 30.0, 
                 max_new_tokens: int = 80,
                 temperature: float = 0.8) -> Tuple[str, List[Dict]]:

        initial_device = self.model.device
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(initial_device)
        generated_ids = input_ids
        
        k_kernel = self._get_target_centroid(target_concepts)
        vocab_sim_to_k = torch.matmul(k_kernel, self.vocab_embeddings.t()).squeeze(0)

        trajectory_log = []
        past_key_values = None
        current_input = input_ids

        for step in range(max_new_tokens):
            with torch.no_grad():
                outputs = self.model(
                    current_input,
                    past_key_values=past_key_values,
                    output_hidden_states=True,
                    use_cache=True
                )
                past_key_values = outputs.past_key_values
                
                logits = outputs.logits[:, -1, :]
                current_device = logits.device
                
                c_t = F.normalize(outputs.hidden_states[-1][:, -1, :], p=2, dim=-1)
                
                k_kernel_local = k_kernel.to(current_device)
                vocab_sim_local = vocab_sim_to_k.to(current_device)
                
                u_raw = torch.matmul(c_t, k_kernel_local.t())
                u_val = ((u_raw + 1.0) / 2.0).item()
                
                # --- Homeostatic Growth Function G(U_t) ---
                diff = u_val - mu
                exponent = -0.5 * (diff / sigma) ** 2
                g_u_val = 2.0 * np.exp(exponent) - 1.0 
                
                # Asymmetric cutoff (dead zone)
                delta_width = sigma * np.sqrt(2.0 * np.log(2.0))
                if u_val < (mu - delta_width):
                    g_u_val = 0.0 
                
                g_u = torch.tensor(g_u_val, dtype=logits.dtype, device=current_device)
                
                bias = 0.0
                if mode == "wild":
                    bias = alpha * g_u * vocab_sim_local

                logits[0] += bias

                # Sampling and Auto-regressive Perplexity
                probs = F.softmax(logits / temperature, dim=-1)
                next_token = torch.multinomial(probs, 1)
                
                current_input = next_token.to(initial_device)
                generated_ids = torch.cat([generated_ids, next_token.to(initial_device)], dim=-1)
                
                next_token_prob = probs[0, next_token.item()].item()
                nll_val = -np.log(max(next_token_prob, 1e-10))
                ppl_t = np.exp(nll_val)
                
                trajectory_log.append({
                    "step": step,
                    "u_potential": round(u_val, 4),
                    "g_growth": round(g_u_val, 4),
                    "ppl_t": ppl_t,
                    "token": self.tokenizer.decode(next_token.item())
                })
                
                if next_token.item() == self.tokenizer.eos_token_id:
                    break
        
        full_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return full_text, trajectory_log
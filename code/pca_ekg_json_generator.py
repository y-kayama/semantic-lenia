# =====================================================================
# Semantic Lenia: Reproducibility & Verification Script for Reviewers
# =====================================================================
import os
import random
import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from sklearn.decomposition import PCA

# ==========================================
# 1. Experimental Setup & Physical Parameters
# ==========================================
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B"
PROMPT = "The secret to a happy life is a lot like"
TARGET_CONCEPTS = ["Computer", "Device", "Memory", "Algorithm", "Data"]

MU = 0.49  # Target Gravity (Peak Activation Distance)
SIGMA = 0.03  # Tolerance Width
ALPHA = 15.0  # Intervention Energy (Coupling Strength)
MAX_TOKENS = 150
GLOBAL_SEED = 42

def set_deterministic_environment(seed=42):
    """Ensure strict deterministic execution for dynamical system reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# ==========================================
# 2. Semantic Lenia Engine (Standalone)
# ==========================================
class SemanticLeniaEngine:
    def __init__(self, model_name, device="cuda"):
        print(f"[*] Loading model and tokenizer: {model_name}...")
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype=torch.float16, device_map=device
        )
        self.model.eval()

        # Retain FP16 precision to prevent type conflicts during projection
        self.vocab_embeddings = F.normalize(
            self.model.get_output_embeddings().weight.detach(), p=2, dim=-1
        )

    def get_target_centroid(self, target_concepts):
        """Extract the geometric centroid vector (k) from the target concept cluster."""
        vectors = []
        for word in target_concepts:
            ids = self.tokenizer(" " + word, add_special_tokens=False).input_ids
            if ids:
                vectors.append(self.vocab_embeddings[ids[0]])
        centroid = torch.stack(vectors).mean(dim=0)
        return F.normalize(centroid, p=2, dim=0).unsqueeze(0)

    def generate_soliton(self):
        input_ids = self.tokenizer(PROMPT, return_tensors="pt").input_ids.to(self.device)

        # Precompute the similarity map (S_k) between the target vector and the entire vocabulary
        k_kernel = self.get_target_centroid(TARGET_CONCEPTS).to(self.device)
        vocab_sim_to_k = torch.matmul(k_kernel, self.vocab_embeddings.t()).squeeze(0)

        u_history = []
        ppl_history = []

        generated_ids = input_ids
        past_key_values = None
        current_input = input_ids

        print("\n" + "=" * 60)
        print("EMERGENT TEXT METAPHORICAL BLENDING (Semantic Lenia):")
        print("=" * 60)
        print(PROMPT, end="", flush=True)

        for step in range(MAX_TOKENS):
            with torch.no_grad():
                outputs = self.model(
                    current_input,
                    past_key_values=past_key_values,
                    output_hidden_states=True,
                    use_cache=True,
                )
                past_key_values = outputs.past_key_values
                logits = outputs.logits[:, -1, :]

                # 1. Calculate Semantic Potential (U_t) from the hidden state
                c_t = F.normalize(outputs.hidden_states[-1][:, -1, :], p=2, dim=-1)
                u_raw = torch.matmul(c_t, k_kernel.t())
                u_val = ((u_raw + 1.0) / 2.0).item()
                u_history.append(u_val)

                # 2. Calculate the growth function G(U_t) with an asymmetric cutoff
                diff = u_val - MU
                exponent = -0.5 * (diff / SIGMA) ** 2
                g_u_val = 2.0 * np.exp(exponent) - 1.0

                delta_width = SIGMA * np.sqrt(2.0 * np.log(2.0))
                if u_val < (MU - delta_width):
                    g_u_val = 0.0  # Dead zone to preserve physical locality

                # Safely cast to match logit dtype (FP16) for multiplication
                g_u = torch.tensor(g_u_val, dtype=logits.dtype, device=logits.device)

                # 3. Non-linear intervention in the macroscopic probability field (Z_steered)
                bias = ALPHA * g_u * vocab_sim_to_k
                logits[0] += bias

                # 4. Sampling and Perplexity (surprisal) calculation
                probs = F.softmax(logits[0] / 0.8, dim=-1)  # Temperature=0.8
                next_token = torch.multinomial(probs, 1).view(1, 1)

                p_t = probs[next_token.item()].item()
                ppl_t = np.exp(-np.log(max(p_t, 1e-10)))
                ppl_history.append(ppl_t)

                token_str = self.tokenizer.decode(next_token[0], skip_special_tokens=True)
                print(token_str, end="", flush=True)

                current_input = next_token.to(self.device)
                generated_ids = torch.cat([generated_ids, current_input], dim=-1)

                if next_token.item() == self.tokenizer.eos_token_id:
                    break

        print("\n\n" + "=" * 60 + "\n")
        return u_history, ppl_history

    def generate_soliton_with_trajectory(self):
        input_ids = self.tokenizer(PROMPT, return_tensors="pt").input_ids.to(self.device)
        k_kernel = self.get_target_centroid(TARGET_CONCEPTS).to(self.device)
        vocab_sim_to_k = torch.matmul(k_kernel, self.vocab_embeddings.t()).squeeze(0)

        # Initialize logging arrays
        u_history = []
        ppl_history = []
        c_history = []
        tokens_history = []

        generated_ids = input_ids
        past_key_values = None
        current_input = input_ids

        print("\n" + "=" * 60)
        print("EMERGENT TEXT METAPHORICAL BLENDING (Semantic Lenia):")
        print("=" * 60)
        print(PROMPT, end="", flush=True)

        # Execute pure autoregressive loop without pre-pass to avoid KV-cache misalignment
        for step in range(MAX_TOKENS):
            with torch.no_grad():
                outputs = self.model(
                    current_input,
                    past_key_values=past_key_values,
                    output_hidden_states=True,
                    use_cache=True,
                )
                past_key_values = outputs.past_key_values
                logits = outputs.logits[:, -1, :]

                # 1. Semantic Potential (U_t)
                c_t = F.normalize(outputs.hidden_states[-1][:, -1, :], p=2, dim=-1)
                u_raw = torch.matmul(c_t, k_kernel.t())
                u_val = ((u_raw + 1.0) / 2.0).item()

                # 2. Growth Function G(U_t)
                diff = u_val - MU
                exponent = -0.5 * (diff / SIGMA) ** 2
                g_u_val = 2.0 * np.exp(exponent) - 1.0

                delta_width = SIGMA * np.sqrt(2.0 * np.log(2.0))
                if u_val < (MU - delta_width):
                    g_u_val = 0.0

                # 3. Macroscopic Intervention
                g_u = torch.tensor(g_u_val, dtype=logits.dtype, device=logits.device)
                bias = ALPHA * g_u * vocab_sim_to_k
                logits[0] += bias

                # 4. Sampling and Perplexity
                probs = F.softmax(logits[0] / 0.8, dim=-1)
                next_token = torch.multinomial(probs, 1).view(1, 1)

                p_t = probs[next_token.item()].item()
                ppl_t = np.exp(-np.log(max(p_t, 1e-10)))

                token_str = self.tokenizer.decode(next_token[0], skip_special_tokens=True)
                print(token_str, end="", flush=True)

                # Record all metrics simultaneously to ensure sequence length alignment
                c_history.append(c_t.cpu().numpy().flatten())
                tokens_history.append(token_str)
                u_history.append(u_val)
                ppl_history.append(ppl_t)

                current_input = next_token.to(self.device)
                generated_ids = torch.cat([generated_ids, current_input], dim=-1)

                if next_token.item() == self.tokenizer.eos_token_id:
                    break

        print("\n\n" + "=" * 60 + "\n")

        # Dimensionality reduction via PCA and JSON export
        self._export_trajectory_to_json(
            c_history, k_kernel, tokens_history, u_history, ppl_history
        )
        return u_history, ppl_history

    def _export_trajectory_to_json(
        self, c_history, k_kernel, tokens_history, u_history, ppl_history
    ):
        print("[*] Projecting latent trajectory into 2D PCA space...")
        trajectory_matrix = np.array(c_history)
        target_vector = k_kernel.cpu().numpy()
        combined_matrix = np.vstack([trajectory_matrix, target_vector])

        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(combined_matrix)

        traj_pca = pca_result[:-1]
        target_pca = pca_result[-1]

        # Combine arrays using zip (safe as all have identical lengths)
        export_data = {
            "target_centroid": {"x": float(target_pca[0]), "y": float(target_pca[1])},
            "trajectory": [
                {
                    "step": i,
                    "x": float(pos[0]),
                    "y": float(pos[1]),
                    "token": token,
                    "u": float(u),      # EKG: Semantic Alignment
                    "ppl": float(ppl),  # EKG: Perplexity
                }
                for i, (pos, token, u, ppl) in enumerate(
                    zip(traj_pca, tokens_history, u_history, ppl_history)
                )
            ],
            "parameters": {"mu": MU, "sigma": SIGMA, "alpha": ALPHA},
        }

        with open("soliton_trajectory.json", "w") as f:
            json.dump(export_data, f, indent=2)
        print("[*] Trajectory and EKG data exported to 'soliton_trajectory.json'")

# ==========================================
# 3. Plotting: The Semantic EKG
# ==========================================
def plot_semantic_ekg(u_values, ppl_values, output_img="Fig_Semantic_Lenia_EKG.png"):
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(12, 7), dpi=200)
    fig.patch.set_facecolor("#0d1117")
    gs = GridSpec(2, 1, height_ratios=[2, 1], hspace=0.1)

    # Panel 1: U_t
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor("#0d1117")
    steps = np.arange(len(u_values))
    ax1.plot(
        steps,
        u_values,
        color="#39FF14",
        linewidth=1.5,
        label=r"Semantic Alignment ($U_t$)",
    )
    ax1.axhline(
        y=MU,
        color="gold",
        linestyle="--",
        linewidth=1,
        label=rf"Target Gravity ($\mu={MU}$)",
    )
    delta = SIGMA * np.sqrt(2 * np.log(2))
    ax1.axhline(
        y=MU - delta,
        color="cyan",
        linestyle=":",
        linewidth=1,
        label=rf"Cutoff Wall ($\mu - \Delta$)",
    )
    ax1.set_title(
        "Artificial Semantic Lifeform EKG (Reviewer Replicability Test)",
        color="white",
        fontsize=14,
        fontweight="bold",
    )
    ax1.set_ylabel("Semantic Potential ($U_t$)", color="white")
    ax1.grid(True, color="#21262d")
    ax1.legend(
        loc="upper right", facecolor="#0d1117", edgecolor="gray", labelcolor="white"
    )

    # Panel 2: PPL
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.set_facecolor("#0d1117")
    ax2.plot(
        steps,
        ppl_values,
        color="#FF007F",
        linewidth=1.0,
        label="Perplexity (Chaos Spikes)",
    )
    ax2.set_yscale("log")
    ax2.set_xlabel("Time Evolution (Generated Tokens)", color="white")
    ax2.set_ylabel("PPL (Log Scale)", color="white")
    ax2.grid(True, color="#21262d")
    ax2.legend(
        loc="upper right", facecolor="#0d1117", edgecolor="gray", labelcolor="white"
    )

    plt.tight_layout()
    plt.savefig(output_img, facecolor=fig.get_facecolor(), bbox_inches="tight")
    print(f"[*] EKG Plot saved successfully as '{output_img}'.")

def main():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    set_deterministic_environment(GLOBAL_SEED)

    engine = SemanticLeniaEngine(model_name=MODEL_NAME, device=device)
    u_vals, ppl_vals = engine.generate_soliton_with_trajectory()

    plot_semantic_ekg(u_vals, ppl_vals)

if __name__ == "__main__":
    main()
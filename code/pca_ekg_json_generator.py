# =====================================================================
# Semantic Lenia: Trajectory / Semantic EKG generator
# Uses the shared semantic_lenia_engine.py implementation.
# =====================================================================
import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from sklearn.decomposition import PCA

from semantic_lenia_engine import (
    UnifiedSemanticLeniaPhase1,
    set_deterministic_environment,
)

MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B"
PROMPT = "The secret to a happy life is a lot like"
TARGET_CONCEPTS = ["Computer", "Device", "Memory", "Algorithm", "Data"]

MU = 0.49
SIGMA = 0.03
ALPHA = 15.0  # Intervention strength
MAX_TOKENS = 150
TEMPERATURE = 0.8
GLOBAL_SEED = 42

OUTPUT_JSON = "soliton_trajectory.json"
OUTPUT_IMAGE = "Fig_Semantic_Lenia_EKG.png"


def generate_trajectory():
    set_deterministic_environment(GLOBAL_SEED)
    engine = UnifiedSemanticLeniaPhase1(
        model_name=MODEL_NAME, use_4bit=False
    )

    text, trajectory = engine.generate(
        prompt=PROMPT,
        target_concepts=TARGET_CONCEPTS,
        mode="wild",
        mu=MU,
        sigma=SIGMA,
        alpha=ALPHA,
        max_new_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        record_hidden_states=True,
    )

    if len(trajectory) < 2:
        raise RuntimeError("Trajectory is too short for 2D PCA.")

    c_history = np.asarray(
        [row["hidden_state"] for row in trajectory], dtype=np.float32
    )
    k_kernel = (
        engine._get_target_centroid(TARGET_CONCEPTS)
        .detach()
        .to("cpu", dtype=np.float32)
        .numpy()
    )

    combined = np.vstack([c_history, k_kernel])
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(combined)
    traj_pca = pca_result[:-1]
    target_pca = pca_result[-1]

    export_data = {
        "description": (
            "PCA visualization of the normalized final-layer hidden-state "
            "trajectory. ppl is instantaneous sampled-token inverse probability."
        ),
        "target_centroid": {
            "x": float(target_pca[0]),
            "y": float(target_pca[1]),
        },
        "trajectory": [
            {
                "step": int(row["step"]),
                "x": float(pos[0]),
                "y": float(pos[1]),
                "token": row["token"],
                "u": float(row["u_potential"]),
                # Backward-compatible dashboard field.
                "ppl": float(row["ppl_t"]),
                "sampled_token_ppl": float(row["sampled_token_ppl"]),
                "token_probability": float(row["token_probability"]),
                "g_growth": float(row["g_growth"]),
            }
            for pos, row in zip(traj_pca, trajectory)
        ],
        "parameters": {
            "model": MODEL_NAME,
            "mu": MU,
            "sigma": SIGMA,
            "alpha": ALPHA,
            "temperature": TEMPERATURE,
            "seed": GLOBAL_SEED,
        },
        "generated_text": text,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"Trajectory data exported to {OUTPUT_JSON}")
    return export_data


def plot_semantic_ekg(data, output_img=OUTPUT_IMAGE):
    u_values = [d["u"] for d in data["trajectory"]]
    ppl_values = [d["ppl"] for d in data["trajectory"]]
    steps = np.arange(len(u_values))

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(12, 7), dpi=200)
    fig.patch.set_facecolor("#0d1117")
    gs = GridSpec(2, 1, height_ratios=[2, 1], hspace=0.1)

    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor("#0d1117")
    ax1.plot(
        steps,
        u_values,
        color="#39FF14",
        linewidth=1.5,
        label=r"Semantic Potential ($U_t$)",
    )
    ax1.axhline(
        y=MU,
        color="gold",
        linestyle="--",
        linewidth=1,
        label=rf"Intervention center ($\mu={MU}$)",
    )
    delta = SIGMA * np.sqrt(2 * np.log(2))
    ax1.axhline(
        y=MU - delta,
        color="cyan",
        linestyle=":",
        linewidth=1,
        label=rf"Dead-zone boundary ($\mu-\Delta$)",
    )
    ax1.set_title(
        "Semantic Lenia: Synchronized Semantic EKG",
        color="white",
        fontsize=14,
        fontweight="bold",
    )
    ax1.set_ylabel(r"Semantic Potential ($U_t$)", color="white")
    ax1.grid(True, color="#21262d")
    ax1.legend(
        loc="upper right",
        facecolor="#0d1117",
        edgecolor="gray",
        labelcolor="white",
    )

    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.set_facecolor("#0d1117")
    ax2.plot(
        steps,
        ppl_values,
        color="#FF007F",
        linewidth=1.0,
        label="Sampled-token inverse probability",
    )
    ax2.set_yscale("log")
    ax2.set_xlabel("Generated token step", color="white")
    ax2.set_ylabel("Token PPL signal (log)", color="white")
    ax2.grid(True, color="#21262d")
    ax2.legend(
        loc="upper right",
        facecolor="#0d1117",
        edgecolor="gray",
        labelcolor="white",
    )

    plt.tight_layout()
    plt.savefig(output_img, facecolor=fig.get_facecolor(), bbox_inches="tight")
    print(f"Semantic EKG plot saved to {output_img}")


def main():
    data = generate_trajectory()
    plot_semantic_ekg(data)


if __name__ == "__main__":
    main()

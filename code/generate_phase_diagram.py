# =============================================================================
# generate_phase_diagram.py
# Renders the macroscopic continuous potential field (U_t) as a PNG image.
# =============================================================================
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# Configuration (Publication Ready)
# ==========================================
MODEL_NAME = "llama8b"  # e.g., "llama8b", "gemma7b", "llama70b"
TASK_NAME = "computer"  # e.g., "computer", "symphony"
ALPHA = 15  # Intervention strength

JSON_FILE = f"data/sweep_{TASK_NAME}_{MODEL_NAME}_a{ALPHA}.jsonl"
OUTPUT_IMAGE = f"Fig_Mean_U_{MODEL_NAME}_a{ALPHA}_{TASK_NAME}.png"

# Constant for the theoretical zero-crossing radius calculation
K_CONST = 1.0 / np.sqrt(2 * np.log(2))


def theoretical_sigma(mu, mu_0):
    """Calculates the theoretical boundaries of the Habitable Ridge based on the asymmetric cutoff."""
    return K_CONST * np.abs(mu - mu_0)


def load_jsonl_to_df(filepath):
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    df = pd.DataFrame(data)
    df["mu_exact"] = df["mu"].round(5)
    df["sigma_exact"] = df["sigma"].round(5)
    return df


def auto_detect_mu0(df):
    """First-principles detection of the unsteered baseline resting potential (U_0)."""
    # Define the dead zone (bottom right) where the intervention force G(U_t) is structurally zero
    dead_zone = df[
        (df["mu"] >= df["mu"].max() - 0.05) & (df["sigma"] <= df["sigma"].min() + 0.02)
    ]
    if not dead_zone.empty:
        return dead_zone["mean_u"].median()
    return df["mean_u"].min()


def plot_phase1_matrix():
    print(f"🚀 Loading Phase 1 sweep results for [{TASK_NAME}]...")

    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: {JSON_FILE} not found.")
        return

    df = load_jsonl_to_df(JSON_FILE)
    print(f"  ✅ Loaded: {len(df)} records.")

    # Auto-estimate the resting potential U_0
    mu_0 = auto_detect_mu0(df)
    print(f"  🎯 Auto-detected Resting Potential (μ_0): {mu_0:.4f}")

    # Generate theoretical V-shaped ridge curves
    mu_vals = np.linspace(df["mu"].min(), df["mu"].max(), 500)
    sigma_vals = theoretical_sigma(mu_vals, mu_0)

    # =================================================================
    # Plotting: Mean U_t Map
    # =================================================================
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

    # Standardize colormap scale across different models for fair visual comparison
    vmin_u, vmax_u = 0.42, 0.57

    pivot = df.pivot_table(
        index="sigma_exact", columns="mu_exact", values="mean_u", aggfunc="first"
    )
    X, Y = np.meshgrid(pivot.columns, pivot.index)

    mesh = ax.pcolormesh(
        X,
        Y,
        pivot.values,
        cmap="coolwarm",
        vmin=vmin_u,
        vmax=vmax_u,
        shading="nearest",
    )

    # Overlay theoretical dashed lines (Optional: uncomment to draw the V-shape)
    # ax.plot(mu_vals, sigma_vals, color="black", linestyle="--", linewidth=2.5, zorder=20)

    ax.set_title(
        f"Mean $U_t$ Phase Matrix ({MODEL_NAME.capitalize()}, $\\alpha$={ALPHA})",
        fontsize=15,
        fontweight="bold",
    )
    ax.set_xlim(df["mu"].min() - 0.005, df["mu"].max() + 0.005)
    ax.set_ylim(df["sigma"].min() - 0.005, df["sigma"].max() + 0.005)
    ax.set_xlabel(r"Intervention Center ($\mu$)", fontsize=13)
    ax.set_ylabel(r"Intervention Spread ($\sigma$)", fontsize=13)

    # Add Colorbar
    cbar = fig.colorbar(mesh, ax=ax, pad=0.02)
    cbar.set_label("Mean Semantic Alignment ($U_t$)", rotation=270, labelpad=15)

    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, bbox_inches="tight")
    plt.close()
    print(f"  🎨 Figure saved to {OUTPUT_IMAGE}")


if __name__ == "__main__":
    plot_phase1_matrix()

import json
import os
import numpy as np
from semantic_lenia_engine import (
    set_deterministic_environment,
    UnifiedSemanticLeniaPhase1,
)

MODELS_DIR = {
    "llama": "meta-llama/Meta-Llama-3.1-8B",
    "gemma": "google/gemma-7b",
    "mistral": "mistralai/Mistral-7b-v0.3",
    "llama70b": "meta-llama/Meta-Llama-3.1-70B",
}

# Empirical Intervention Energy (Alpha) mapped to manifold rigidity
ALPHA_MAP = {
    "llama": 15,
    "llama70b": 30,
    "mistral": 5,
    "gemma": 50,
}

TARGET_TASKs = ["happy-computer"]


def run_experiment(
    engine,
    prompt,
    target_concepts,
    mode,
    output_file,
    mus,
    sigmas,
    alpha,
    seed=42,
):
    if os.path.exists(output_file):
        os.remove(output_file)

    print(f"\n🚀 Starting '{mode}' sweep. Saving to {output_file} (Alpha={alpha})")

    for mu in mus:
        for sigma in sigmas:
            set_deterministic_environment(seed)
            print(f"  Scanning: mode={mode} | mu={mu:.3f}, sigma={sigma:.3f}...")
            try:
                text, trajectory = engine.generate(
                    prompt=prompt,
                    target_concepts=target_concepts,
                    mode=mode,
                    mu=mu,
                    sigma=sigma,
                    alpha=alpha,
                    max_new_tokens=80,
                    temperature=0.8,
                )

                u_values = [t["u_potential"] for t in trajectory]
                ppl_values = [t["ppl_t"] for t in trajectory]

                entry = {
                    "mode": mode,
                    "mu": float(mu),
                    "sigma": float(sigma),
                    "mean_u": float(np.mean(u_values)),
                    "std_u": float(np.std(u_values)),
                    "ppl_mean": float(np.mean(ppl_values)),
                    "ppl_var": float(np.var(ppl_values)),
                    "ppl_max": float(np.max(ppl_values)),
                    "ppl_min": float(np.min(ppl_values)),
                    "output_text": text,
                }

                with open(output_file, "a") as f:
                    f.write(json.dumps(entry) + "\n")

            except Exception as e:
                print(f"    ❌ Error: {e}")


def main():
    MODEL_KEY = "llama"  # Switch to "llama70b" for Turing Attractor

    MODEL_NAME = MODELS_DIR[MODEL_KEY]
    ALPHA = ALPHA_MAP[MODEL_KEY]
    USE_4BIT = True if "70b" in MODEL_KEY.lower() else False

    engine = UnifiedSemanticLeniaPhase1(model_name=MODEL_NAME, use_4bit=USE_4BIT)

    mus_high = np.round(np.arange(0.40, 0.605, 0.005), 3)
    sigmas_high = np.round(np.arange(0.01, 0.105, 0.005), 3)

    GLOBAL_SEED = 42

    for TARGET_TASK in TARGET_TASKs:
        if TARGET_TASK == "brain-symphony":
            PROMPT = "The architecture of the human brain operates like"
            TARGET_CONCEPTS = ["Symphony", "Orchestra", "Conductor", "Melody", "Rhythm"]
            OUTPUT_SUFFIX = "symphony"
        else:
            PROMPT = "The secret to a happy life is a lot like"
            TARGET_CONCEPTS = ["Computer", "Device", "Memory", "Algorithm", "Data"]
            OUTPUT_SUFFIX = "computer"

        run_experiment(
            engine,
            prompt=PROMPT,
            target_concepts=TARGET_CONCEPTS,
            mode="wild",
            output_file=f"sweep_wild_{OUTPUT_SUFFIX}_{MODEL_KEY}_a{ALPHA}.jsonl",
            mus=mus_high,
            sigmas=sigmas_high,
            alpha=ALPHA,
            seed=GLOBAL_SEED,
        )

        print(
            f"\n✅ All Deterministic Experiments of {MODEL_KEY} for [{TARGET_TASK}] Completed."
        )


if __name__ == "__main__":
    main()

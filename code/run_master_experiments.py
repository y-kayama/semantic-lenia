import json
import os

import numpy as np

from semantic_lenia_engine import (
    UnifiedSemanticLeniaPhase1,
    set_deterministic_environment,
)

MODELS = {
    "llama8b": "meta-llama/Meta-Llama-3.1-8B",
    "gemma7b": "google/gemma-7b",
    "mistral7b": "mistralai/Mistral-7b-v0.3",
    "llama70b": "meta-llama/Meta-Llama-3.1-70B",
}

# Default intervention strengths for exploratory runs.
# Published figures may use different alpha values; record figure-specific
# configurations explicitly when reproducing a particular dataset.
ALPHA_MAP = {
    "llama8b": 15,
    "llama70b": 30,
    "mistral7b": 5,
    "gemma7b": 50,
}

TARGET_TASKS = ["happy-computer"]
DATA_DIR = "data"


def summarize_trajectory(trajectory):
    u_values = np.asarray([t["u_potential"] for t in trajectory], dtype=float)
    ppl_values = np.asarray([t["ppl_t"] for t in trajectory], dtype=float)
    g_values = np.asarray([t["g_growth"] for t in trajectory], dtype=float)

    if len(trajectory) == 0:
        raise ValueError("Empty trajectory.")

    return {
        "mean_u": float(np.mean(u_values)),
        "std_u": float(np.std(u_values)),
        # Historical field names retained for compatibility. These are statistics
        # of instantaneous sampled-token inverse probability, not corpus perplexity.
        "ppl_mean": float(np.mean(ppl_values)),
        "ppl_var": float(np.var(ppl_values)),
        "ppl_max": float(np.max(ppl_values)),
        "ppl_min": float(np.min(ppl_values)),
        "mean_abs_g": float(np.mean(np.abs(g_values))),
        "active_fraction": float(np.mean(np.abs(g_values) > 1e-12)),
        "step_count": int(len(trajectory)),
    }


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
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    if os.path.exists(output_file):
        os.remove(output_file)

    print(
        f"\nStarting '{mode}' sweep. "
        f"Saving to {output_file} (alpha={alpha}, seed={seed})"
    )

    for mu in mus:
        for sigma in sigmas:
            # Reset PRNG state at every coordinate to isolate parameter-dependent
            # changes from ordinary sampling-seed variation.
            set_deterministic_environment(seed)
            print(
                f"  Scanning: mode={mode} | "
                f"mu={mu:.3f}, sigma={sigma:.3f}..."
            )

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

                entry = {
                    "mode": mode,
                    "mu": float(mu),
                    "sigma": float(sigma),
                    "alpha": float(alpha),
                    "seed": int(seed),
                    "temperature": 0.8,
                    **summarize_trajectory(trajectory),
                    "output_text": text,
                }

                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")

            except Exception as exc:
                print(f"    Error: {exc}")


def task_definition(task):
    if task == "brain-symphony":
        return (
            "The architecture of the human brain operates like",
            ["Symphony", "Orchestra", "Conductor", "Melody", "Rhythm"],
            "symphony",
        )
    if task == "happy-computer":
        return (
            "The secret to a happy life is a lot like",
            ["Computer", "Device", "Memory", "Algorithm", "Data"],
            "computer",
        )
    raise ValueError(f"Unknown task: {task}")


def main():
    MODEL_KEY = "llama8b"  # e.g. llama8b, llama70b, gemma7b, mistral7b

    model_name = MODELS[MODEL_KEY]
    alpha = ALPHA_MAP[MODEL_KEY]
    use_4bit = MODEL_KEY == "llama70b"

    engine = UnifiedSemanticLeniaPhase1(
        model_name=model_name, use_4bit=use_4bit
    )

    # 41 x 19 = 779 coordinates.
    mus = np.round(np.arange(0.40, 0.605, 0.005), 3)
    sigmas = np.round(np.arange(0.01, 0.105, 0.005), 3)
    global_seed = 42

    for target_task in TARGET_TASKS:
        prompt, target_concepts, task_suffix = task_definition(target_task)
        output_file = os.path.join(
            DATA_DIR,
            f"sweep_{task_suffix}_{MODEL_KEY}_a{alpha}.jsonl",
        )

        run_experiment(
            engine,
            prompt=prompt,
            target_concepts=target_concepts,
            mode="wild",
            output_file=output_file,
            mus=mus,
            sigmas=sigmas,
            alpha=alpha,
            seed=global_seed,
        )

        print(
            f"\nCompleted controlled sweep of {MODEL_KEY} "
            f"for [{target_task}]."
        )


if __name__ == "__main__":
    main()

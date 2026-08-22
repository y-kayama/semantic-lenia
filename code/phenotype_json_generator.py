# =============================================================================
# phenotype_json_generator.py
# Generates JSON data for the interactive web-based phenotype phase diagram.
# =============================================================================
import csv
import json
import os

JSONL_FILE = "data/sweep_computer_llama8b_a15.jsonl"
CSV_FILE = "data/sweep_computer_llama8b_a15.csv"
OUTPUT_FILE = "data/heatmap_data_computer_llama8b_a15.json"

# Six macroscopic phenotype families are shown publicly.
# Homeostatic Soliton is split into 3a / 3b internal display subtypes.
PHASE1_TAXONOMY = {
    "1": {"z": 0, "name": "Baseline Drift", "color": "#808080"},
    "2": {"z": 1, "name": "Semantic Crystallization", "color": "#dc143c"},
    "3a": {
        "z": 2,
        "name": "Homeostatic Soliton (Deep Isomorphism)",
        "color": "#FFD700",
    },
    "3b": {
        "z": 3,
        "name": "Homeostatic Soliton (Surface Metaphor)",
        "color": "#90ee90",
    },
    "3c": {"z": 4, "name": "Abductive Leap", "color": "#00ffff"},
    "4": {"z": 5, "name": "Attractor Hijack", "color": "#4169e1"},
    "5": {"z": 6, "name": "Syntactic Rupture", "color": "#ff0000"},
}


def generate_heatmap_json():
    print("Generating interactive JSON for web portal...")

    full_texts = {}
    if not os.path.exists(JSONL_FILE):
        raise FileNotFoundError(JSONL_FILE)

    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            key = (
                round(float(record["mu"]), 3),
                round(float(record["sigma"]), 3),
            )
            full_texts[key] = record["output_text"]

    data_points = []
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(CSV_FILE)

    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mu = round(float(row["mu"]), 3)
            sigma = round(float(row["sigma"]), 3)
            mean_u = float(row["mean_u"])
            ppl_var = float(row["ppl_var"])
            state_key = row["corrected_state"].strip().lower()

            if state_key not in PHASE1_TAXONOMY:
                raise ValueError(
                    f"Unknown corrected_state={state_key!r} "
                    f"at mu={mu}, sigma={sigma}"
                )

            full_text = full_texts.get(
                (mu, sigma), row.get("text_snippet", "")
            )
            state_info = PHASE1_TAXONOMY[state_key]

            data_points.append(
                {
                    "mu": mu,
                    "sigma": sigma,
                    "z_val": state_info["z"],
                    "state_name": state_info["name"],
                    "mean_u": round(mean_u, 3),
                    "ppl_var": round(ppl_var, 1),
                    "full_text": full_text,
                }
            )

    mus = sorted({d["mu"] for d in data_points})
    sigmas = sorted({d["sigma"] for d in data_points})

    z_matrix = [[None for _ in mus] for _ in sigmas]
    hover_matrix = [[None for _ in mus] for _ in sigmas]
    custom_matrix = [[None for _ in mus] for _ in sigmas]

    for d in data_points:
        x_idx = mus.index(d["mu"])
        y_idx = sigmas.index(d["sigma"])
        z_matrix[y_idx][x_idx] = d["z_val"]

        hover_matrix[y_idx][x_idx] = (
            f"<b style='color:#ffffff;'>{d['state_name']}</b><br>"
            f"μ: {d['mu']}, σ: {d['sigma']}<br>"
            f"U_t: {d['mean_u']}, PPL_var: {d['ppl_var']}"
        )

        safe_text = (
            d["full_text"]
            .replace("\n", "<br>")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
        custom_matrix[y_idx][x_idx] = safe_text

    export_data = {
        "x": mus,
        "y": sigmas,
        "z": z_matrix,
        "text": hover_matrix,
        "customdata": custom_matrix,
    }

    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False)

    print(f"Interactive JSON saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_heatmap_json()

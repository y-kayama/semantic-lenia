# =============================================================================
# phenotype_json_generator.py
# Generates the JSON data for the interactive web-based phase diagram.
# =============================================================================
import csv
import json
import os

# Configuration Parameters (Edit these to match your target substrate)
JSONL_FILE = "./sweep_computer_llama8b_a15.jsonl"
CSV_FILE = "./sweep_computer_llama8b_a15.csv"
OUTPUT_FILE = "./heatmap_data_computer_llama8b_a15.json"

PHASE1_TAXONOMY = {
    "1": {"z": 0, "name": "Baseline Drift", "color": "#808080"},
    "2": {"z": 1, "name": "Semantic Crystallization", "color": "#dc143c"},
    "3a": {
        "z": 2,
        "name": "Homeostatic Soliton (Deep Isomorphism)",
        "color": "#FFD700",
    },  # Gold for 3a
    "3b": {
        "z": 3,
        "name": "Homeostatic Soliton (Surface Metaphor)",
        "color": "#90ee90",
    },
    "3c_true_leap": {"z": 4, "name": "Abductive Leap", "color": "#00ffff"},
    "3d_spurious_escape": {
        "z": 5,
        "name": "Spurious Escape",
        "color": "#4b0082",
    },  # Indigo for spurious
    "4": {"z": 6, "name": "Attractor Hijack", "color": "#4169e1"},
    "5": {"z": 7, "name": "Syntactic Rupture", "color": "#ff0000"},
}


def generate_heatmap_json():
    print(f"🚀 Generating interactive JSON for web portal...")

    full_texts = {}
    if not os.path.exists(JSONL_FILE):
        print(f"❌ Error: {JSONL_FILE} not found.")
        return

    with open(JSONL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            mu_key = round(float(record["mu"]), 3)
            sigma_key = round(float(record["sigma"]), 3)
            full_texts[(mu_key, sigma_key)] = record["output_text"]

    data_points = []
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: {CSV_FILE} not found.")
        return

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mu = round(float(row["mu"]), 3)
            sigma = round(float(row["sigma"]), 3)
            mean_u = float(row["mean_u"])
            ppl_var = float(row["ppl_var"])
            state_key = row["corrected_state"].strip().lower()

            full_text = full_texts.get((mu, sigma), row.get("text_snippet", ""))

            # Fallback for undefined states
            if state_key not in PHASE1_TAXONOMY:
                if "3c" in state_key:
                    state_key = "3c_true_leap"
                elif "5" in state_key:
                    state_key = "5"
                elif "2" in state_key:
                    state_key = "2"
                else:
                    state_key = "1"

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

    mus = sorted(list(set([d["mu"] for d in data_points])))
    sigmas = sorted(list(set([d["sigma"] for d in data_points])))

    # Initialize matrices
    z_matrix = [[None for _ in mus] for _ in sigmas]
    hover_matrix = [[None for _ in mus] for _ in sigmas]
    custom_matrix = [[None for _ in mus] for _ in sigmas]

    for d in data_points:
        x_idx = mus.index(d["mu"])
        y_idx = sigmas.index(d["sigma"])
        z_matrix[y_idx][x_idx] = d["z_val"]

        # Minimal tooltips for the hover box
        tooltip = (
            f"<b style='color:#ffffff;'>{d['state_name']}</b><br>"
            f"μ: {d['mu']}, σ: {d['sigma']}<br>"
            f"U_t: {d['mean_u']}, PPL_var: {d['ppl_var']}"
        )
        hover_matrix[y_idx][x_idx] = tooltip

        # HTML encoding for full text delivery to JS
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

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False)

    print(f"✅ Interactive JSON saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_heatmap_json()

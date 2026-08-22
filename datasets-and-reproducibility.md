---
layout: page
title: "Datasets and Reproducibility"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) &nbsp;&bull;&nbsp; [Phase Diagram](./phase-diagram.html) &nbsp;&bull;&nbsp; [Dashboard](./dashboard.html) &nbsp;&bull;&nbsp; [Substrate Rigidity](./substrate-rigidity.html) &nbsp;&bull;&nbsp; [Lifespan & Aging](./lifespan-and-aging.html) &nbsp;&bull;&nbsp; [Gallery](./phenotype-gallery.html) &nbsp;&bull;&nbsp; [Datasets](./datasets-and-reproducibility.html) &nbsp;&bull;&nbsp; [Roadmap](./future-roadmap.html)

# Datasets and Reproducibility

---

## 💾 Raw Trajectory Datasets

In accordance with open science principles, the complete raw trajectory datasets (including 779 parameter sweep coordinates, PCA projections, and Semantic EKG logs) are fully open-sourced.
While the provided scripts are configured for the Llama-3.1-8B model to ensure accessibility and single-GPU reproducibility for reviewers, we also provide the pre-computed raw trajectory data for the 70B 'Turing Attractor'. Researchers can directly load this JSON into dashboard.html to visualize the heavy manifold dynamics described in the paper.

- **Download Link: https://github.com/y-kayama/semantic-lenia/**

```text
code/
 ├── semantic_lenia_engine.py       # Unified Semantic Lenia intervention engine (8B/70B)
 ├── run_master_experiments.py      # Macro-parameter sweep script for data generation
 ├── taxonomy_evaluator.py          # LLM-as-a-Judge evaluation & trajectory diagnostics
 ├── generate_phase_diagram.py      # Renders U_t continuous heatmaps & Phenotype matrices
 ├── phenotype_json_generator.py    # JSON export for Phenotype matrices from taxonomy data
 ├── pca_ekg_json_generator.py      # Single trajectory generation & JSON export for EKG
 ├── dashboard.html                 # Interactive real-time trajectory & EKG dashboard
 └── heatmap.html                   # Pre-rendered interactive macroscopic phase diagram

data/
 ├── sweep_computer_llama8b_a15.jsonl       # 8B Happy->Computer task, 779-grid sweep (α=15)
 ├── sweep_computer_llama8b_a15.csv         # Analyzed results of the 8B Computer sweep
 ├── sweep_computer_llama70b_a30.jsonl      # 70B Happy->Computer task, 779-grid sweep (α=30)
 ├── sweep_computer_llama70b_a30.csv        # Analyzed results of the 70B Computer sweep
 ├── sweep_symphony_llama8b_a15.jsonl       # 8B Brain->Symphony task, 779-grid sweep (α=15)
 ├── sweep_symphony_llama8b_a15.csv         # Analyzed results of the 8B Symphony sweep
 └── turing_soliton_70b_mu_0-49_sigma_0-03.json # Orbital data for the 70B Turing Soliton
```

- **Data License:** The datasets are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. You are free to share and adapt the data, provided you give appropriate credit.

### 📝 Note on Dataset State Codes

In our provided raw datasets (`.csv` and `.json`), you may notice alphanumeric codes (e.g., `3a`, `3c`, `5`) under the `corrected_state` column. These are our internal programmatic codes used for fine-grained tracking of the continuous dynamics.

For clarity when cross-referencing the dataset with **Table 1 in our manuscript**, please use the following mapping:

| Phenotype in Manuscript                | Dataset Code | Internal Meaning                            |
| :------------------------------------- | :----------- | :------------------------------------------ |
| **Baseline Drift** (Gray)              | `1`          | Pure unsteered trajectory.                  |
| **Semantic Crystallization** (Crimson) | `2`          | Low-variability repetitive regime.          |
| **Homeostatic Soliton** (Light Green)  | `3a`         | Deep Isomorphism (Perfect fusion).          |
| **Homeostatic Soliton** (Green)        | `3b`         | Surface Metaphor (Associative analogies).   |
| **Abductive Leap** (Cyan)              | `3c`         | Stable slingshot into a third-party domain. |
| **Attractor Hijack** (Blue)            | `4`          | Domain collapse.                            |
| **Syntactic Rupture** (Red)            | `5`          | Complete structural disintegration.         |

---

## 🚀 Usage Guide

We provide the **core generation, parameter-sweep, taxonomy, phase-diagram, and trajectory-visualization scripts** in the `code/` directory, together with the raw datasets used in the study. Additional dynamical analyses reported in the manuscript, including selected recurrence, autocorrelation, hardware-divergence, and long-horizon analyses, are being prepared for release.

### 1. Generating a Single Trajectory & EKG Dashboard

If you want to observe a specific semantic soliton and extract its PCA trajectory & Semantic EKG (used for our Real-time Dashboard), use the standalone generator.

**Step 1: Configure**
Open `code/pca_ekg_json_generator.py` and directly edit the physical parameters at the top of the file:

```python
# Edit these parameters in the script
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B"
MU = 0.49      # Peak Activation Distance
SIGMA = 0.03   # Tolerance Width
ALPHA = 15.0   # Intervention strength
```

**Step 2: Run**

```bash
python code/pca_ekg_json_generator.py
```

(This will output soliton_trajectory.json)

**Step 3: Visualize**
Edit json_path in dashboard.html to point to your new JSON file, then open the HTML in your browser.

### 2. Running Macroscopic Parameter Sweeps

To map the entire latent manifold and reproduce the phase diagrams (The Taxonomy), we provide a master sweep script. This script automatically runs across a grid of (μ,σ) coordinates.

**Step 1: Configure**
Open `code/run_master_experiments.py` and directly edit the physical parameters:

```python
# Edit these parameters in the script
ALPHA_MAP = {
    "llama8b": 15.0,
    "llama70b": 30.0,
    "mistral7b": 5.0,
    "gemma7b": 50.0,
}

TARGET_TASKs = ["happy-computer"] # "brain-symphony"

# inside main()
MODEL_KEY = "llama8b"  # "llama8b", "gemma7b", "mistral7b", "llama70b"

```

> **Configuration note:** The values in `ALPHA_MAP` are default exploratory settings. Individual published figures may use dataset-specific intervention strengths; the corresponding $\alpha$ value is stated in each figure caption and dataset filename.

**Step 2: Run**

```bash
python code/run_master_experiments.py
```

(This iteratively generates text across the parameter grid and outputs a `.jsonl` file containing raw data and trajectory diagnostics. The historical `ppl_t` field denotes instantaneous sampled-token inverse probability, not conventional sequence perplexity.)

### 3. Generating the Phase Diagrams

You can generate two types of phase diagrams from your sweep results.

**(A) Static Potential Heatmap ($\bar U_t$)**

**Step 1: Configure**
Open `code/generate_phase_diagram.py` and specify the parameters matching your sweep results:

```python
MODEL_NAME = "llama8b"       # e.g., "llama8b", "gemma7b", "llama70b"
TASK_NAME = "computer"       # e.g., "computer", "symphony"
ALPHA = 15                   # Intervention strength
```

**Step 2: Run**

```bash
python code/generate_phase_diagram.py
```

(This generates a static .png heatmap image.)

**(B) Macroscopic Interactive Phase Diagram (The Taxonomy)**

**Step 1: LLM-as-a-Judge Evaluation**
Prepare a local LLM (ex. google/gemma-4-31b via LM Studio) to build a taxonomy for a sweep data .
Open `code/taxonomy_evaluator.py` and set your local LLM "MODEL_NAME":

This script is designed to be run from the command line. You should specify input_file and output_csv files name via command-line arguments.
The task ("brain-symphony" or "happy-computer") is automatically selected from the input_file name you specified:

```bash
python code/taxonomy_evaluator.py --input_file data/sweep_computer_llama8b_a15.jsonl --output_csv data/sweep_computer_llama8b_a15.csv
```

**Step 2: Generate JSON for Web**
Open `code/phenotype_json_generator.py` and update the file paths to match your substrate:

```python
# Configuration Parameters (Edit these to match your target substrate)
JSONL_FILE = "data/sweep_computer_llama8b_a15.jsonl"
CSV_FILE = "data/sweep_computer_llama8b_a15.csv"
OUTPUT_FILE = "data/heatmap_data_computer_llama_a15.json"
```

Then, run the generator:

```bash
python code/phenotype_json_generator.py
```

**Step 3: Visualize**
Open `code/heatmap.html` in an editor, update const json_path to point to the newly generated JSON, and open the HTML in your browser to explore the interactive taxonomy.

```javascript
// Target JSON dataset generated by phenotype_json_generator.py
const json_path = "./heatmap_data_computer_llama8b_a15.json";
```

---

## 🦋 Hardware and Software Environment

To support **controlled trajectory-level reproducibility**, we strictly recorded and constrained the hardware and software environment. Exact token sequences can be sensitive to small numerical differences between GPU architectures, particularly near Habitable Ridge boundaries (see Section 4.7 of the manuscript), so hardware isolation was used for the primary exploratory sweeps.

### Hardware Specifications:

- **Lightweight Substrates (Llama-3.1-8B, Gemma-7B):** All exploratory parameter sweeps and phase diagram generations were strictly isolated and executed on a single **NVIDIA RTX Pro 4500 (Blackwell architecture)** to prevent any cross-architecture floating-point divergence.
- **Heavy Substrate (Llama-3.1-70B):** Due to VRAM constraints imposed by the massive 70-billion parameter scale, the model was quantized to 4-bit precision (NF4) using BitsAndBytes. Inference was distributed across a heterogeneous dual-GPU setup consisting of an **NVIDIA RTX Pro 4500** (Primary, CUDA:0) and an **NVIDIA RTX 3090** (Ampere architecture, CUDA:1). Device-mismatch during dynamic tensor operations was prevented via real-time device alignment protocols implemented in our custom steering processor.

### Software and Compilation Environment:

- **Python:** 3.13.14
- **PyTorch:** 2.10.0+cu130
- **CUDA Compilation Tools:** Release 13.1, V13.1.115 (Build cuda_13.1.r13.1/compiler.37061995_0)
  All pseudo-random number generators (PRNG seeds) across Python, NumPy, and PyTorch (including CUDA deterministic flags) were locked to a global seed of $42$. The fixed seed was intentionally used to isolate parameter-dependent trajectory changes from stochastic sampling variation and to enable trajectory-level comparison under a controlled environment. The softmax sampling temperature was fixed at $0.8$ across exploratory and scaling generations.

---

## ✍️ How to Cite

If you use our codebase, datasets, or conceptual framework in your research, please cite our arXiv preprint.

**Preprint Citation (BibTeX):**

```bibtex
@article{kayama2026semantic,
  author    = {Kayama, Yoshihiko},
  title     = {Semantic Lenia: Emergence of Homeostatic Solitons within the Semantic Space of Large Language Models},
  journal   = {arXiv preprint arXiv:2608.11657},
  year      = {2026},
  url       = {https://arxiv.org/abs/2608.11657}
}
```

# Semantic Lenia: Emergence of Homeostatic Solitons in LLM Logit Space

Official academic repository and interactive resources for the paper:  
**"Semantic Lenia: Emergence of Homeostatic Solitons within the Semantic Space of Large Language Models"**

---

## 🌐 Interactive Web Portal

The interactive companion website, featuring trajectory visualizers, dynamic phase diagrams, and detailed specimen galleries, is live at:  
👉 **[https://y-kayama.github.io/semantic-lenia/](https://y-kayama.github.io/semantic-lenia/)**

---

## 🌟 Executive Summary

**Semantic Lenia** bridges the fields of Continuous Artificial Life (Lenia) and Natural Language Processing. Traditionally, decoding-time steering of Large Language Models (LLMs) is dominated by open-loop or unidirectional interventions. Under sufficiently strong steering, generation can enter low-variability repetitive regimes that we operationally describe as **"Semantic Crystallization"**.

By introducing a state-dependent non-linear steering force governed by a homeostatic growth function $G(U_t)$, we observe bounded **"Semantic Soliton"** regimes in the macroscopic logit-space intervention framework. These trajectories sustain semantic variation around target conceptual centroids while resisting immediate collapse into repetitive or syntactically degraded states. We interpret them as dissipative-like homeostatic dynamics.

**Implementation note:** The released code measures $\mathbf{c}_t$ from the final Transformer layer at the current final sequence position. The historical `ppl_t` signal is the instantaneous inverse probability of the sampled token after intervention and temperature scaling; it is not conventional sequence perplexity or Shannon entropy.

---

## 📁 Repository Structure

This repository contains both the source files for our Jekyll-powered companion website and the underlying research assets. The current public release contains the core Semantic Lenia generation, parameter-sweep, taxonomy, and trajectory-visualization pipeline. Additional analysis scripts used for selected dynamical diagnostics will be released separately:

- **`.md` files (root)**: The 8-page academic portal, detailing our theoretical framework, taxonomy, substrate rigidity comparisons (Llama vs. Gemma), long-horizon aging observations (lifespan up to 800 tokens), and next-generation roadmaps.
- **`data/`**: The complete raw trajectory datasets, consisting of 779 coordinates from our parameter sweeps, PCA projections, and Semantic EKG trajectory logs.
- **`assets/`**: High-resolution figures, phase diagrams, and animated interactive HTML objects (PCA orbit dashboards and taxonomy heatmaps).

---

## 💻 Local Web Development (Jekyll)

If you wish to host and preview the companion web portal locally:

1. Ensure you have **Ruby** and **Bundler** installed.
2. Install dependencies:

    ```bash
    bundle install
    ```

3. Run the local Jekyll server:

    ```bash
    bundle exec jekyll serve
    ```

4. Open your browser and navigate to:

    ```text
    http://localhost:4000/semantic-lenia/
    ```

---

## 📄 Licensing & Open Science

To support open science, this repository uses a dual-licensing scheme:

- **Codebase & Software:** Apache License 2.0 (see `LICENSE`).
- **Research Datasets:** Creative Commons Attribution 4.0 International (CC BY 4.0) (see `LICENSE_DATA.md`).

---

## ✍️ Citation (Preprint)

**"Semantic Lenia: Emergence of Homeostatic Solitons within the Semantic Space of Large Language Models"**  
arXiv:2608.11657.

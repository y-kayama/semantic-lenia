# Semantic Lenia: Emergence of Homeostatic Solitons in LLM Logit Space

Official academic repository and interactive resources for the paper:  
**"Semantic Lenia: Emergence of Homeostatic Solitons within the Semantic Space of Large Language Models"**

---

## 🌐 Interactive Web Portal

The interactive companion website, featuring trajectory visualizers, dynamic phase diagrams, and detailed specimen galleries, is live at:  
👉 **[https://y-kayama.github.io/semantic-lenia/](https://y-kayama.github.io/semantic-lenia/)**

---

## 🌟 Executive Summary

**Semantic Lenia** bridges the fields of Continuous Artificial Life (Lenia) and Natural Language Processing. Traditionally, steering Large Language Models (LLMs) at decoding time treats generation as a static optimization problem, which often forces the trajectory into local point attractors—a state of low grammatical entropy we define as **"Semantic Crystallization"** (degenerative token looping).

By introducing a non-linear steering force governed by a homeostatic growth function $G(U_t)$, we facilitate the self-organization of **"Autonomous Semantic Solitons"** within the macroscopic logit space. These dissipative structures orbit target conceptual centroids, maintaining a delicate, far-from-equilibrium tension that guarantees high semantic alignment without structural collapse.

---

## 📁 Repository Structure

This repository contains both the source files for our Jekyll-powered companion website and the underlying research assets:

- **`.md` files (root)**: The 8-page academic portal, detailing our theoretical framework, taxonomy, substrate rigidity comparisons (Llama vs. Gemma), thermodynamic aging (lifespan up to 800 tokens), and next-generation roadmaps.
- **`data/`**: The complete raw trajectory datasets, consisting of 779 coordinates from our parameter sweeps, PCA projections, and thermodynamic EKG logs.
- **`assets/`**: High-resolution figures, phase diagrams, and animated interactive HTML objects (PCA orbit dashboards and taxonomy heatmaps).

---

## 💻 Local Web Development (Jekyll)

If you wish to host and preview the companion web portal locally:

1. Ensure you have **Ruby** and **Bundler** installed.
2. Install dependencies:
    ```bash
    bundle install
    Run the local Jekyll server:
    Open your browser and navigate to http://localhost:4000/semantic-lenia/.
    📄 Licensing & Open-Science Compliance
    To support open science while maintaining rigorous legal and technical standards, this repository adopts a dual-licensing scheme:
    Codebase & Software: Licensed under the Apache License 2.0. (See the LICENSE file in the root).
    Research Datasets: Licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license. (See LICENSE_DATA.md or refer to the dataset guidelines conforming to the Japan Link Center (JaLC) standards).
    ✍️ Citation (Preprint)
    "Semantic Lenia: Emergence of Homeostatic Solitons within the Semantic Space of Large Language Models"
    (arXiv:2608.11657).
    ```

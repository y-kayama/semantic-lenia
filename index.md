---
layout: page
title: "Semantic Lenia: Home"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) &nbsp;&bull;&nbsp; [Phase Diagram](./phase-diagram.html) &nbsp;&bull;&nbsp; [Dashboard](./dashboard.html) &nbsp;&bull;&nbsp; [Substrate Rigidity](./substrate-rigidity.html) &nbsp;&bull;&nbsp; [Lifespan & Aging](./lifespan-and-aging.html) &nbsp;&bull;&nbsp; [Gallery](./phenotype-gallery.html) &nbsp;&bull;&nbsp; [Datasets](./datasets-and-reproducibility.html) &nbsp;&bull;&nbsp; [Roadmap](./future-roadmap.html)

# Semantic Lenia: Emergence of Homeostatic Solitons in LLM Logit Space

## 🌟 Executive Summary

**Semantic Lenia** transforms Large Language Model (LLM) inference into a continuous dynamical system within the macroscopic logit space. Traditionally, decoding-time steering treats inference as a static optimization problem, which often forces the generation into local point attractors—a state we define as **"Crystallization"** (degenerative token looping).

By injecting a non-linear steering force governed by a homeostatic growth function $G(U_t)$, we facilitate the self-organization of **"Autonomous Semantic Solitons"**. These dissipative structures orbit the target conceptual centroid, maintaining a delicate far-from-equilibrium tension that guarantees grammatical entropy and high semantic alignment without structural collapse.

This site serves as the interactive companion to our manuscript, designed to provide reviewers and researchers with **verifiable, reproducible, and interactive evidence** of these emergent dynamics.

---

## 📐 Mathematical Formulation

At its core, Semantic Lenia projects the continuous, self-regulating principles of continuous Cellular Automata (Lenia) onto the probability simplex of autoregressive language generation.

### 1. Semantic Potential ($U_t$)

The state of the text generation is tracked by the context hidden vector $\mathbf{c}_t \in \mathbb{R}^D$. We measure its proximity to the target concept by calculating the normalized cosine similarity against a **Target Kernel Centroid** $\mathbf{k}$:

$$\mathbf{k} = \frac{1}{\left\|\sum_{w \in C} \mathbf{w}\right\|_2} \sum_{w \in C} \mathbf{w} \quad (\text{Eq. 1})$$

$$U_t = \frac{\text{sim}(\mathbf{c}_t, \mathbf{k}) + 1.0}{2.0} \quad (\text{Eq. 2})$$

Where $C$ represents a multi-token cluster representing a semantic neighborhood (e.g., `{"Computer", "Device", "Memory", "Algorithm", "Data"}`).

_Methodological Note:_ Using a multi-token cluster acts as a semantic low-pass filter to denoise word-specific syntactic biases and avoids the singularity-induced exclusion of single-word targets.

### 2. Homeostatic Growth Function ($G(U_t)$)

Rather than pushing the model unidirectionally, our growth function regulates both attraction (steering toward the concept) and repulsion (preventing literal crystallization):

$$G(U_t) = \begin{cases} 0, & \text{if } U_t < \mu - \Delta \\ 2 \cdot \exp\left(-\frac{(U_t - \mu)^2}{2\sigma^2}\right) - 1, & \text{if } U_t \geq \mu - \Delta \end{cases} \quad (\text{Eq. 3})$$

Where:

- $\mu$ defines the **peak activation distance**.
- $\sigma$ controls the **tolerance width**.
- $\Delta = \sigma \sqrt{2 \ln 2}$ represents the **zero-crossing radius**.
- States falling below $U_t < \mu - \Delta$ enter a **"dead zone"** ($G(U_t) = 0$), preserving natural baseline generation far from the target.

### 3. Unified State Update Rule

The steered output logits $\mathbf{Z}_{\text{steered}} \in \mathbb{R}^N$ are computed at each token generation step by superimposing the semantic force onto the model's base manifold:

$$\mathbf{Z}_{\text{steered}} = \mathbf{Z}_{\text{base}} + \alpha \cdot G(U_t) \cdot \mathbf{S}_k \quad (\text{Eq. 5})$$

Where $\mathbf{Z}_{\text{base}}$ represents the **Syntactic Inertia** (the model's massive inherent drive to maintain grammatically and deterministically coherent sequences), $\alpha$ is the **intervention energy**, and $\mathbf{S}_k \in \mathbb{R}^N$ is the vocabulary-wide similarity projection field.

---

## 🗺️ Interactive Exploration Sections

To thoroughly examine the properties of Semantic Lenia, we have prepared dedicated pages exploring its global and microscopic properties:

- **[Phase Diagram & Taxonomy](./phase-diagram.html)**: Explore the exhaustive $779$-point parameter sweep mapping the macroscopic "habitability" of the $70\text{B}$ Llama-3.1 manifold, detailing our rigorous classification tree of emergent cognitive phenotypes.
- **[Real-time Trajectory & EKG Dashboard](./dashboard.html)**: Observe the microscopic orbital path of hidden states ($\mathbf{c}_t$) projected onto 2D PCA spaces, tracked concurrently with a "Semantic EKG" monitor showing real-time homeostatic breathing and linguistic entropy.

---

## 🛠️ Environment & Reproducibility

To ensure deterministic reproducibility across different environments, we provide the complete Python scripts and a list of required dependencies. You can easily set up the environment using `pip`.

```bash
# Clone the repository
git clone https://github.com/y-kayama/semantic-lenia.git
cd semantic-lenia

# Install required packages
pip install -r requirements.txt
```

---

## ✍️ Academic Citation

### Semantic Lenia: Emergence of Homeostatic Solitons in LLM Logit Space

This is the interactive companion web portal for the paper:  
**"Semantic Lenia: Emergence of Homeostatic Solitons within the Semantic Space of Large Language Models"** (arXiv:2608.11657).

The codebase of this project is licensed under the **Apache License 2.0**, while the associated research datasets are shared under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.
These guidelines and data-sharing protocols strictly conform to the **Japan Link Center (JaLC)** standards for open data sharing and reproducibility.

## 📚 References

1. **Arora, S., Liang, Y., & Ma, T. (2017).** A simple but tough-to-beat baseline for sentence embeddings. _International Conference on Learning Representations_.
2. **Berlekamp, E. R., Conway, J. H., & Guy, R. K. (1982).** _Winning ways for your mathematical plays_ (Vol. 2). AK Peters.
3. **Chan, B. W.-C. (2019).** Lenia: Biology of artificial life. _Complex Systems_, 28(3), 251–286.
4. **Chan, B. W.-C. (2020).** Lenia and expanded universe. _Artificial Life Conference Proceedings_, 32, 221–229.
5. **Ho, J., & Salimans, T. (2022).** Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_.
6. **Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. (2019).** The curious case of neural text degeneration. _arXiv preprint arXiv:1904.09751_.
7. **Krause, B., Gotmare, A. D., McCann, B., Keskar, N. S., Joty, S., Socher, R., & Naik, N. F. (2021).** GeDi: Generative discriminator guided sequence generation. Findings of the Association for Computational Linguistics: EMNLP 2021, 4929–4952.
8. **Liu, A., Sap, M., Lu, X., Swayamdipta, S., Bhagavatula, C., Smith, N. A., & Choi, Y. (2021).** Dexperts: Decoding-time controlled text generation with experts and anti-experts. _Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics_, 6691–6706.
9. **Rosch, E. (1978).** Principles of categorization. In _Cognition and categorization_ (pp. 27–48). Lawrence Erlbaum Associates.
10. **Turner, A. M., Thiergart, L., Leech, G., Udell, D., Vazquez, J. J., Mini, U., & MacDiarmid, M. (2024).** Activation addition: Steering language models without optimization.
11. **Zou, A., Phan, L., Chen, S. L., Campbell, J., Guo, P., Ren, R., Pan, A., Yin, X., Mazeika, M., Dombrowski, A.-K., et al. (2023).** Representation engineering: A top-down approach to ai transparency. _arXiv preprint arXiv:2310.01405_.

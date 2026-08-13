---
layout: page
title: "Phase Diagram & Taxonomy"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) | [Phase Diagram](./phase-diagram.html) | [Dashboard](./dashboard.html) | [Substrate Rigidity](./substrate-rigidity.html) | [Lifespan & Aging](./lifespan-and-aging.html) | [Gallery](./phenotype-gallery.html) | [Datasets](./datasets-and-reproducibility.html) | [Roadmap](./future-roadmap.html)

# Phase Diagram & Taxonomy

To map the geometric landscape of machine cognition under non-linear steering, we perform high-resolution $(\mu, \sigma)$ parameter sweeps. This page explains the resulting phase diagrams and provides a mathematical taxonomy of the self-organizing trajectories.

---

## 🗺️ Macroscopic Interactive Phase Diagram

Under mild intervention energy ($\alpha=15$) on our exploratory substrate (**Meta-Llama-3.1-8B**), the continuous hidden manifold exhibits high elasticity. This allows the steering force to successfully counteract syntactic inertia, carving out a smooth, V-shaped **"Habitable Ridge"** where stable limit cycles (Homeostatic Solitons) autonomously self-organize.
Here is the interactive phase diagram extracted from our grid sweeps of 779 individual simulation points:

<iframe src="./assets/heatmap_8b_a15.html" width="100%" height="1000px" style="border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></iframe>
<p align="right"><a href="./assets/heatmap_8b_a15.html" target="_blank">↗️ Open Phase Diagram in Full Screen</a></p>
  <p align="justify"><span style="font-weight: bold;">Figure 2-(Left): Emergent phenotype matrices mapping the spatial self-organization of trajectories for the Happy &rarr; Computer task under &alpha; = 15.</span> Llama-3.1-8B illustrates high elastic habitability, featuring a structured band of stable Homeostatic Solitons (green) along the Habitable Ridge, bounded by Attractor Hijacks (blue).</p>

---

## 🧬 Taxonomy of Emergent Phenotypes

To transition from qualitative evaluation to a rigorous, automated classification framework, we train a shallow decision tree classifier using trajectory-level metrics: **Mean Semantic Potential ($\bar{U}_t$)**, **Perplexity Variance ($PPL_{\text{var}}$)**, and **Step Count ($T$)**.

The **Perplexity Variance** mathematically quantifies linguistic entropy:

$$PPL_{\text{var}} = \frac{1}{T} \sum_{t=1}^T (PPL_t - \overline{PPL})^2 \quad (\text{Eq. 6})$$

A sudden drop to $PPL_{\text{var}} < 10.0$ indicates a total loss of linguistic entropy, signaling repetitive grammatical loops.

- **Baseline Drift**: $\bar U_t < \mu-\Delta$, $PPL_{var} \geq 10.0$
- **Homeostatic Soliton**: $\mu-\Delta \leq \bar U_t \leq \mu+\Delta$, $PPL_{var} \geq 10.0$ (Stable Limit Cycle / Breathing)
- **Abductive Leap**: Escape ($\bar U_t < \mu-\Delta $), $PPL_{var} \geq 10.0$ (Hyperbolic Orbit / Slingshot)
- **Attractor Hijack**: $\bar U_t > \mu+\Delta $, $PPL_{var} \geq 10.0$ (Domain Collapse)
- **Semantic Crystallization**: $T \to \infty, \lim_{t \to \infty} PPL_{var}(t) < 10.0$ (Thermal Death / Infinite Loop)
- **Syntactic Rupture**: Grammatical Rupture

## 🦋 Hardware-Level Reproducibility at the Edge of Chaos

Infinitesimal FP16 rounding errors ($\sim 10^{-4}$) between NVIDIA Ampere (RTX 3090) and Blackwell (RTX Pro 4500) GPU architectures cause macroscopic trajectory bifurcations. The spatial distribution of these hardware-induced bifurcations perfectly traces the boundaries of the V-shaped "Habitable Ridge," physically proving that our non-linear boundaries operate at the true **"edge of chaos."**

<p align="center">
    <img src="./assets/Fig4_hardware-induced_bifurcations.png" alt="Hardware-induced trajectory bifurcations" width="60%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
  <br>
  <p align="justify"><span style="font-weight: bold;">Figure 4: Spatial distribution of hardware-induced trajectory bifurcations (Llama-3.1-8B, Happy &rarr; Computer, &alpha; = 15.0).</span> Each plotted point represents a parameter coordinate where infinitesimal FP16 rounding errors (10<sup>-4</sup>) between Blackwell and Ampere GPU architectures cause identical initial states to diverge into distinct text paths. The distribution perfectly traces the boundaries of the V-shaped ``Habitable Ridge'' mapped in Figure 2-(Left), with a visibly thicker bifurcation band along the left boundary (lower &mu;) induced by the steep, asymmetric repulsive barrier.</p>
</p>

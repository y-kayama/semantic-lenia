---
layout: page
title: "Real-time Trajectory & EKG Dashboard"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) &nbsp;&bull;&nbsp; [Phase Diagram](./phase-diagram.html) &nbsp;&bull;&nbsp; [Dashboard](./dashboard.html) &nbsp;&bull;&nbsp; [Substrate Rigidity](./substrate-rigidity.html) &nbsp;&bull;&nbsp; [Lifespan & Aging](./lifespan-and-aging.html) &nbsp;&bull;&nbsp; [Gallery](./phenotype-gallery.html) &nbsp;&bull;&nbsp; [Datasets](./datasets-and-reproducibility.html) &nbsp;&bull;&nbsp; [Roadmap](./future-roadmap.html)

# Real-time Trajectory & Semantic EKG Dashboard

To examine whether macroscopic homeostatic classifications correspond to structured latent-state motion, we zoom in on trajectories of the hidden state $\mathbf{c}_t$. This page presents a synchronized monitoring dashboard and quantitative trajectory metrics for Semantic Lenia.

---

## 🖥️ Synchronized Monitoring Dashboard

Our real-time dashboard links low-dimensional trajectory geometry to token-level sequence statistics. It synchronizes the projected latent trajectory, semantic potential, perplexity-related signals, and generated text (Press Play or use the slider):

<iframe src="./assets/dashboard_turing.html" width="100%" height="1000px" style="border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></iframe>
<p align="right"><a href="./assets/dashboard_turing.html" target="_blank">↗️ Open Dashboard in Full Screen</a></p>

The dashboard is divided into three key synchronized panels:

1. **2D PCA Trajectory (Left)**: Shows the continuous hidden state vector $\mathbf{c}_t$ projected onto the first two principal components (PC1, PC2). The target conceptual centroid is marked as a gold star ($\star$).
2. **Semantic Potential $U_t$ (Top Right)**: Tracks the normalized similarity to the target concept. The oscillatory motion within the habitable boundaries ($\mu \pm \Delta$) is interpreted as a homeostatic "breathing" pattern associated with resistance to immediate crystallization.
3. **Log Perplexity & Text Output (Bottom)**: Tracks token-level surprise together with the generated sequence. Changes in this signal can be compared with attractive and repulsive phases of the feedback loop.

### 🗺️ Interactive Macroscopic Phase Diagram

#### Substrate Scaling: The 70B "Turing Attractor"

In our experiments, the 70B model behaves as a higher-resistance substrate than the 8B model, exhibiting substantially greater apparent **Syntactic Inertia** under comparable intervention settings. Under near-critical intervention strength ($\alpha = 30.0$), most sampled coordinates remain in Baseline Drift, producing an operational **Inertial Barrier** (the dominant gray region).

Yet, near $\mu = 0.490, \sigma = 0.030$, a localized Homeostatic Soliton regime appears consistently in the mapped phase diagram. We refer to this representative trajectory as the **"Turing Attractor"**. It produces a deeply integrated conceptual blend involving Turing's historical tragedy while remaining dynamically distinct from nearby baseline and crystallized regimes.

_Hover over the interactive phase diagram below to explore how this semantic soliton is exclusively isolated within the heavy manifold._

<iframe src="./assets/heatmap_70b_a30.html" width="100%" height="900px" style="border:1px solid #30363d; border-radius: 6px;"></iframe>
<p align="right"><a href="./assets/heatmap_70b_a30.html" target="_blank">↗️ Open Phase Diagram in Full Screen</a></p>
<p align="justify"><span style="font-weight: bold;">Figure 5-(Right): Phase diagrams of Llama-3.1-70B under near-critical intervention (&alpha; = 30.0).</span> The phenotype matrix shows a dominant Baseline Drift region (gray) together with a localized Homeostatic Soliton basin (light green) at (&mu;, &sigma;)=(0.490, 0.030) and (0.495, 0.025).</p>
---

## 📐 Microscopic Trajectory Metrics

To quantify representative trajectories, we analyze a fixed observation window $W=150$ using the mean projected radius $\bar r$, the radius variance $\mathrm{Var}(r)$, and Dist-3 lexical diversity. These quantities characterize different aspects of the observed motion, but they do **not** by themselves establish a strict periodic orbit or deterministic chaos.

Under mild intervention ($\alpha = 15.0$), conventional linear steering ($\mathbf{Z}_{\text{base}} + \alpha \mathbf{S}_k$) can enter repetitive loops within approximately 50 steps (Dist-3 = $0.342$ in the corresponding 8B experiment). Under the high-intervention 70B comparison shown below ($\alpha=50.0$), linear steering collapses immediately, whereas the Semantic Lenia trajectories remain active up to the maximum observation horizon.

| Method / Phenotype       | Trajectory Lifespan | Mean Radius ($\bar{r}$) | Radius Var. | Dist-3 |
| :----------------------- | :------------------ | :---------------------- | :---------- | :----- |
| **Baseline (Unsteered)** | $> 150$ (Ongoing)   | 1.4033                  | 0.00014     | 0.910  |
| **Linear Steering**      | 1 (Collapsed)       | 1.3477                  | 0.00006     | 0.070  |
| **Homeostatic Soliton**  | $> 150$ (Observed)  | 1.3936                  | 0.00036     | 0.978  |
| **Abductive Leap**       | $> 150$ (Observed)  | 1.4170                  | 0.00009     | 0.889  |
| **Attractor Hijack**     | $> 150$ (Observed)  | 1.3818                  | 0.00048     | 0.965  |

The comparison shows that, under the tested conditions, Semantic Lenia maintains dynamically varying trajectories with high lexical diversity, whereas strong linear steering collapses rapidly. The radius statistics are best interpreted as low-dimensional trajectory descriptors rather than proof of a closed orbit.

### Dynamical Interpretation

Additional autocorrelation and recurrence analyses reported in the manuscript rule out a simple strict periodic limit cycle and are consistent with complex, aperiodic, recurrent dynamics. We therefore use the term **chaotic-like** as an operational interpretation. A rigorous demonstration of deterministic chaos would require direct instability estimates (for example Lyapunov-type or equivalent invariants adapted to the hybrid discrete-continuous setting).

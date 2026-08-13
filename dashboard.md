---
layout: page
title: "Real-time Trajectory & EKG Dashboard"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) | [Phase Diagram](./phase-diagram.html) | [Dashboard](./dashboard.html) | [Substrate Rigidity](./substrate-rigidity.html) | [Lifespan & Aging](./lifespan-and-aging.html) | [Gallery](./phenotype-gallery.html) | [Datasets](./datasets-and-reproducibility.html) | [Roadmap](./future-roadmap.html)

# Real-time Trajectory & Thermodynamic EKG Dashboard

To confirm whether macroscopic homeostatic states are mere statistical aggregates or governed by precise, deterministic physical trajectories, we zoom in to the microscopic orbital paths of the hidden state $\mathbf{c}_t$. This page showcases our synchronized monitoring dashboard and quantifies the orbital mechanics of Semantic Lenia.

---

## 🖥️ Synchronized Monitoring Dashboard

Our real-time dashboard bridges the gap between spatial geometry and text sequence semantics. It visualizes the precise correlation between the trajectory's physical movement and the model's internal stress (Press Play or use the slider):

<iframe src="./assets/dashboard_turing.html" width="100%" height="1000px" style="border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></iframe>
<p align="right"><a href="./assets/dashboard_turing.html" target="_blank">↗️ Open Dashboard in Full Screen</a></p>

The dashboard is divided into three key synchronized panels:

1. **2D PCA Trajectory (Left)**: Shows the continuous hidden state vector $\mathbf{c}_t$ projected onto the first two principal components (PC1, PC2). The target conceptual centroid is marked as a gold star ($\star$).
2. **Semantic Potential $U_t$ (Top Right)**: Tracks the real-time distance to the target concept. You can observe the rhythmic "breathing" movement within the habitable boundaries ($\mu \pm \Delta$), physically preventing crystallization.
3. **Log Perplexity & Text Output (Bottom)**: Tracks the instantaneous linguistic stress. When the trajectory approaches too close to the target, perplexity spikes (repulsive phase), introducing syntactic diversity before returning to a smoother attractive state.

### 🗺️ Interactive Macroscopic Phase Diagram

#### Substrate Scaling: The 70B "Turing Attractor"

Due to its immense parameter scale, the 70B model acts as a heavy gravitational substrate, possessing an exponentially larger Syntactic Inertia. Under near-critical energy ($\alpha = 30.0$), it deflects most interventions, creating a massive **Inertial Barrier** (the dominant gray region).

Yet, at precisely $\mu = 0.490, \sigma = 0.030$, the applied force perfectly balances the massive syntactic inertia, allowing a structurally invariant **"Turing Attractor"** to stubbornly self-organize. This highly localized resonance basin generates profound conceptual blends, such as the deep isomorphism of Turing's historical tragedy.

_Hover over the interactive phase diagram below to explore how this pristine limit cycle is exclusively isolated within the heavy manifold._

<iframe src="./assets/heatmap_70b_a30.html" width="100%" height="900px" style="border:1px solid #30363d; border-radius: 6px;"></iframe>
<p align="right"><a href="./assets/heatmap_70b_a30.html" target="_blank">↗️ Open Phase Diagram in Full Screen</a></p>
<p align="justify"><span style="font-weight: bold;">Figure 5-(Right): Thermodynamic phase diagrams of Llama-3.1-70B under near-critical scaling pressure (&alpha; = 30.0).</span> The phenotype matrix demonstrates that the model's massive syntactic inertia acts as a rigid barrier (Baseline Drift, gray), pierced exclusively by the stable, structurally robust ``Turing Attractor'' (light green) self-organizing at the precise coordinates of (&mu;, &sigma;)=(0.490, 0.030) and (0.495, 0.025).</p>
---

## 📐 Microscopic Orbital Metrics

To quantify the macroscopic homeostatic states, we analyzed the microscopic orbital mechanics over a fixed observation window $W=150$. Notably, even under a mild intervention ($\alpha = 15.0$), linear steering ($\mathbf{Z}_{\text{base}} + \alpha \cdot \mathbf{S}_k$) inherently lacks boundary constraints, forcing the trajectory to collapse into repetitive loops (e.g., “Data Data Data...”) within approximately 50 steps and causing a severe drop in lexical diversity (Dist-3 = $0.342$). The table below proves that Semantic Lenia sustains dynamic limit cycles across distinct cognitive phenotypes, whereas linear steering causes immediate structural collapse. Calculations are performed on **Meta-Llama-3.1-70B Base** ($\alpha = 50.0$):

| Method / Phenotype       | Trajectory Lifespan | Mean Radius ($\bar{r}$) | Radius Var. | Ang. Vel. ($\bar{\omega}$) | Dist-3 |
| :----------------------- | :------------------ | :---------------------- | :---------- | :------------------------- | :----- |
| **Baseline (Unsteered)** | $> 150$ (Ongoing)   | 1.4033                  | 0.00014     | 0.9854 rad/s               | 0.910  |
| **Linear Steering**      | 1 (Collapsed)       | 1.3477                  | 0.00006     | 0.0660 rad/s               | 0.070  |
| **Homeostatic Soliton**  | $> 150$ (Stable)    | 1.3936                  | 0.00036     | 1.2949 rad/s               | 0.978  |
| **Abductive Leap**       | $> 150$ (Stable)    | 1.4170                  | 0.00009     | 1.0898 rad/s               | 0.889  |
| **Attractor Hijack**     | $> 150$ (Stable)    | 1.3818                  | 0.00048     | 1.1504 rad/s               | 0.965  |

Linear steering instantly crushes angular velocity to $0.0660$ rad/s and causes catastrophic lexical decay (Dist-3 = $0.070$). In stark contrast, Semantic Lenia actively repels the singularity, sustaining robust "breathing" oscillations and high rotational momentum ($\bar{\omega} > 1.0$ rad/s) far-from-equilibrium.

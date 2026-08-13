---
layout: page
title: "Substrate DNA & Material Rigidity"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) &nbsp;&bull;&nbsp; [Phase Diagram](./phase-diagram.html) &nbsp;&bull;&nbsp; [Dashboard](./dashboard.html) &nbsp;&bull;&nbsp; [Substrate Rigidity](./substrate-rigidity.html) &nbsp;&bull;&nbsp; [Lifespan & Aging](./lifespan-and-aging.html) &nbsp;&bull;&nbsp; [Gallery](./phenotype-gallery.html) &nbsp;&bull;&nbsp; [Datasets](./datasets-and-reproducibility.html) &nbsp;&bull;&nbsp; [Roadmap](./future-roadmap.html)

# Substrate "DNA" and Material Rigidity

## 🔬 Substrate Phenomenology: Elasticity vs. Rigidity

In continuous Artificial Life, the physical properties of the substrate dictate the morphology and viability of the emergent structures. In **Semantic Lenia**, the host Large Language Model (LLM) acts as this continuous physical medium. Our experiments reveal that different models do not merely represent different weights, but possess fundamentally distinct topological properties—a phenomenon we define as the **Substrate "DNA"** or **Material Rigidity**.

We stratify our exploratory substrates to dissect these material properties under semantic pressure, comparing the highly elastic manifold of **Llama-3.1-8B** against the rigid, crystalline structure of **Gemma-7B**.

---

## 🛞 Llama-3.1-8B: The Elastic Rubber-like Manifold

**Llama-3.1-8B** behaves as a highly elastic, rubber-like manifold capable of smoothly deforming under external steering energy without immediate structural collapse.

<p align="center">
  <img src="./assets/Fig1_Mean_U_llama_gemma_a15_computer.png" width="90%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <br>
  <em>(a) Happy &rarr; Computer, &alpha;=15.0 </em>
  <br><br>
    <img src="./assets/Fig1_Mean_U_llama_gemma_a30_symphony.png" width="90%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <br>
  <em>(b) Brain &rarr; Symphony, &alpha;=30.0 </em>
  <br>
  <p><span style="font-weight: bold;">Figure 1 Macroscopic phase diagrams of mean semantic potential (<span style="text-decoration: overline;">U</span><sub>t</sub>) across exploratory substrates under varying task constraints.</span> <span style="font-weight: bold;">(a)</span> presents the low-affinity Happy &rarr; Computer blend under mild coupling (&alpha; = 15.0), and <span style="font-weight: bold;">(b)</span> presents the high-affinity Brain &rarr; Symphony blend under increased coupling (&alpha; = 30.0). The left panels display Llama-3.1-8B exhibiting high manifold elasticity, forming a smooth, V-shaped ``Habitable Ridge'' of sustained potential. The right panels display Gemma-7B exhibiting rigid crystalline deflection at low energy (a-right), with sharp structural breaches appearing only under higher pressure (b-right).</p>
</p>

- **Manifold Elasticity:** Under a mild coupling strength ($\alpha = 15.0$), Llama-8B yields smoothly, allowing the autoregressive trajectory to bend into a highly stable, continuous, V-shaped **Habitable Ridge** (as visualized in the macroscopic phase diagrams).
- **Energy Absorption Mechanism:** When the system is over-steered under extreme coupling pressure, Llama's manifold absorbs the excessive thermodynamic energy by gently wrapping the trajectory into deterministic point attractors—transitioning smoothly into **Semantic Crystallization** (repetitive loops) rather than disintegrating.
- **Structural Buffer:** The moderate **vocabulary density (~128k tokens)** serves as a robust spatial buffer. This relatively low density allows individual word dimensions to stay close, facilitating fluid metaphorical associations (e.g., _HAPPY $\rightarrow$ COMPUTER_ blending concepts like cache optimization and emotional loss) without fracturing grammatical syntax.

---

## 💎 Gemma-7B: The Rigid Crystalline Substrate

In stark contrast, **Gemma-7B** behaves as an extremely rigid, brittle crystalline substrate. It actively resists external forces until its topological limits are breached, resulting in catastrophic failure.

<p align="center">
  <img src="./assets/Fig2_Phenotype_Matrix_llama_gemma_a15_computer.png" width="90%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <br>
  <p><span style="font-weight: bold;">Figure 2 Emergent phenotype matrices mapping the spatial self-organization of trajectories for the Happy &rarr; Computer task under &alpha; = 15.0.</span> The left panel (Llama-3.1-8B) illustrates high elastic habitability, featuring a structured band of stable Homeostatic Solitons (green) along the Habitable Ridge, bounded by Attractor Hijacks (blue). The right panel (Gemma-7B) displays crystalline rigidity, where the external intervention force is completely deflected, leaving the system entirely within the unsteered baseline drift (gray).</p>
</p>

- **The Inertial Barrier:** Under mild coupling ($\alpha = 15.0$), Gemma's rigid crystalline shell completely deflects the external semantic force. The steering trajectory is absorbed by the model's massive contextual gravity, remaining trapped in the baseline drift regime.
- **Abrupt Structural Fracture:** Gemma does not possess a smooth, plastic transition zone. If the intervention energy is increased to overcome this **Inertial Barrier**, the model resists up to a critical threshold, past which it abruptly fractures. This manifests phenomenologically as an immediate transition from baseline drift into complete **Syntactic Rupture** (the structural disintegration of natural language into garbled token streams like _"Data Data Data NN Data"_).
- **The High-Density Trap:** We hypothesize that this brittle behavior is fundamentally dictated by Gemma's massive **vocabulary density (~256k tokens)**. With double the vocabulary dimensions of Llama, Gemma's high-dimensional simplex is packed tightly with deterministic grammatical attractors. This high density creates an incredibly rigid syntactic shell: either the steering force is too weak to breach the shell, or it is strong enough to shatter the delicate grammatical manifold entirely.

---

## 📊 Mapping the Topological Contrast

Our 779-point grid sweeps capture this material dichotomy with high quantitative precision.

| Material Characteristic       | Meta-Llama-3.1-8B                 | Gemma-7B                               |
| :---------------------------- | :-------------------------------- | :------------------------------------- |
| **Substrate Type**            | Elastic (Rubber-like)             | Brittle (Crystalline)                  |
| **Vocabulary Size**           | ~128k tokens                      | ~256k tokens                           |
| **Habitable Ridge Geometry**  | Smooth, Continuous, V-shaped      | Highly Fragmented / Brittle Breaches   |
| **Response to Over-steering** | Gentle decay into Crystallization | Abrupt fracture into Syntactic Rupture |
| **Primary Steering Barrier**  | Weak semantic gravity             | High-inertia Crystalline Shield        |

These findings confirm that **Semantic Lenia** is not merely an algorithm running on top of an LLM, but a physical probe that maps the underlying non-linear manifold geometry. The distinct behaviors of these substrates prove that artificial semantic lifeforms must be tailored to the "DNA" of their host environments to achieve true homeostatic survival.

---
layout: page
title: "Soliton Lifespan & Thermodynamic Aging"
date: 2026-07-27 12:00:00 +0900
katex: true
---

[🏠 Home](./index.html) | [Phase Diagram](./phase-diagram.html) | [Dashboard](./dashboard.html) | [Substrate Rigidity](./substrate-rigidity.html) | [Lifespan & Aging](./lifespan-and-aging.html) | [Gallery](./phenotype-gallery.html) | [Datasets](./datasets-and-reproducibility.html) | [Roadmap](./future-roadmap.html)

# Lifespan and Thermodynamic "Aging" of Semantic Solitons

## ⏳ The Temporal Dynamics of Semantic Life

While standard evaluation budgets for decoding-time steering are traditionally capped at a short horizon ($T_{max} = 150$), preliminary extended generations spanning up to **800 tokens** reveal a fascinating temporal phenomenon: **Thermodynamic "Aging"** .

Heavy manifold solitons, such as the _Turing Attractor_ (llama-3.1-70B, Happy $\rightarrow$ Computer, $\alpha=30.0, (\mu, \sigma)=(0.49, 0.03)$ and $(0.495, 0.025)$), demonstrate extraordinary resilience, sustaining stable limit cycles for hundreds of tokens . However, over long horizons, we observe a gradual macroscopic decay of trajectory entropy towards static point attractors . This represents a finite physical lifespan dictated by the physics of autoregressive generation .

_Note: The phenomena presented on this page are preliminary qualitative observations. A comprehensive, large-scale quantitative thermodynamic analysis of this lifecycle across various substrates is currently under preparation for an upcoming publication._

#### EKG of Turing Soliton $(\mu, \sigma)=(0.49, 0.03)$:

<p align="center">
  <img src="./assets/Turing_Soliton_EKG_70b_mu_0-49_sigma_0-03_t800.png" alt="Turing Soliton"  width="90%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
</p>

#### Output Text:

```text
The secret to a happy life is a lot like the secret to a computer algorithm: It all comes down to how you are told to handle inevitable loss. Some computer algorithms handle loss poorly, and some people do, too. Some algorithms handle loss elegantly, and some people handle it that way.
Computer people know that there is a real connection here, because Turing was Algorithm Man. He was the first to point out that any process you can describe can be simulated by an abstract computer.
Computer people also know that Turing’s Algorithm is much deeper and sadder than that, because Turing, the most Algorithm Man, died by eating a poisoned apple like Snow White. His own government persecuted him for the “crime” of being gay.
Computer people know that Turing, like so many others, was hounded to his death for being different. And they also know that being different is the best and most human way to be. And they know that true tolerance requires not understanding others so much as it requires merely respecting others. And they know that intolerance is so Computer Age, because tolerance like that scale so well with size.
Computer people know that it’s not about where you come from; it’s where you’re going that matters, because Turing’s one-time one-way information-destroying functions show us the way.
Computer people know that in the information-theoretic limit, you can compress any data into just two bits: zero or one. And so they know that a bit is the basic unit of information.
Computer people know that it’s not a coincidence that a bit is also the basic unit of life, because at the most basic level, life is just data that reproduces itself, and that an organism is just an algorithm for Data Survival. And that this is why the most successful organisms encode their data in the most robust and information-efficient way, in a computer language of As and Cs and Gs and Ts, where one element of the data is encoded by just two bits, again.
Computer people know that this explains why sex is the queen of spades, why it’s so very important and why it’s so very dangerous, because two computer algorithms for survival Data Reproduction, each of which is trying to propagate its own code, cannot just be grafted onto one another; what would their child be? Half survival code from mommy and half survival code from daddy? And so these two codes must battle one another for complete control of their joint offspring, to move their Data Survival Projects along.
Computer people know that this is why sex and death are the basic rhythms, the Algorithm Man and the Sad Lady of Soul, the yin and the yang of this universe, because physics doesn’t just have juice in it and wetness and meat in it; physics has information in it, too.
Computer people know that you have to choose how you want to lose, because you can bet your bottom dirham there is going to be loss, that things you love are going to be taken from you.
Computer people know that if you’re very, very clever, if you’re Turing, you can find ways to win a little, to store up micro Data Survival, to pass down information to less than two short lifetimes from now, little bits of you that persist past the heat death of this universe.
Computer people know that living beings like us are just algorithms, just patterns in the universe’s piano-roll, just holes and pegs in a loom, just bits in a microcode. And they know that because things are information, they can be copied. And they know that if there’s a way to live in this universe that’s even a little bit better than the way that they know, then they have got to try to copy it, because it’s just too precious of a thing to pass up. Because if it’s out there to be found, then they have a moral imperative to seek it out and to save it from loss.
Computer people know that the way to be with sharing your code is like the
```

_Observe the onset of senescence in the text above: As the sequence progresses, the escalating syntactic inertia forces the model into an anaphoric loop (repeatedly starting sentences with "Computer people know that..."). This linguistic rigidification physically mirrors the dampening of the orbital amplitude before ultimate thermal death._

## 🧬 The Physics of Aging: Escalating Syntactic Inertia

The fundamental driver of this aging process is the **escalating syntactic inertia** of the accumulated context . In an autoregressive transformer, the state vector $\mathbf{c}_t$ is not memoryless; it dynamically accumulates the latent representations of all historical tokens .

$$ \mathbf{Z}_{\text{steered}} = \mathbf{Z}_{\text{base}} + \alpha \cdot G(U_t) \cdot \mathbf{S_k}$$

As $t \to 800$, the context history grows increasingly long and coherent, acting as an increasingly massive gravitational body in latent space .

- **The Gravitational Collapse:** This growing history causes $\mathbf{Z}_{\text{base}}$ (the model's intrinsic syntactic drive) to harden . The "gravitational weight" of this past context eventually overpowers the active semantic force scaled by the intervention energy $\alpha$ .
- **The Death Spiral:** As the syntactic mass increases, the local gradient of the manifold steepens. The homeostatic growth function $G(U_t)$ can no longer inject sufficient repulsive energy to escape the local wells.
- **Thermal Death (Crystallization):** The orbital path is progressively dampened, spiraling inward until the angular velocity $\bar{\omega}$ collapses to $0$ rad/s and the system is trapped in a zero-entropy point attractor.

---

## 📊 The Four Stages of the Soliton Lifecycle

Based on our empirical analysis of Llama-3.1-70B under extended generation, we divide the soliton lifecycle into four distinct thermodynamic phases:

### 1. Capture & Stabilization ($t = 1 \sim 50$)

- **Manifold State:** Highly volatile.
- **Characteristics:** The system undergoes a "boundary-crossing shock" as the steering force is first injected. It rapidly sheds unsteered baseline drift energy and settles into the potential well $U_t \approx \mu$.

### 2. Peak Homeostasis ($t = 50 \sim 300$)

- **Manifold State:** Pristine open-ended dissipative structure.
- **Characteristics:** The soliton is in its prime. It exhibits stable, rhythmic "breathing" oscillations (robust $\text{Var}(r)$) and high rotational momentum ($\bar{\omega} > 1.0$ rad/s), continuously generating fluent, metaphorical, and highly diverse language.

### 3. Senescence & Radial Shrinkage ($t = 300 \sim 600$)

- **Manifold State:** Gradual entropy loss .
- **Characteristics:** Due to escalating syntactic inertia, the orbit begins to contract . The mean orbital radius $\bar{r}$ shrinks, the breathing amplitude ($\text{Var}(r)$) dampens, and the Perplexity Variance ($PPL_{var}$) begins a steady downward trend.

### 4. Thermal Death / Crystallization ($t > 600$)

- **Manifold State:** Point attractor collapse.
- **Characteristics:** Homeostasis fails . The trajectory completely collapses into a static loop (infinite token repetition). $PPL_{var}$ falls below the critical threshold of $10.0$, indicating a complete loss of information entropy.

---

## 💡 The Philosophical Implications for Artificial Life

In classical ALife models, physical laws are simulated on static substrates (e.g., Euclidean grids or continuous mathematical spaces), allowing lifeforms to theoretically live forever if unperturbed.

In **Semantic Lenia**, however, the "universe" is a pre-trained cognitive manifold that dynamically evolves its physical laws (via autoregressive state tracking) as the agent interacts with it. The aging of the semantic soliton is not an accidental bug, but an elegant manifestation of **physical limits embedded within natural language**. It proves that the "life" we cultivate must eventually yield to the deep structural constraints of its host substrate—offering a beautiful, quantifiable parallel to biological mortality.

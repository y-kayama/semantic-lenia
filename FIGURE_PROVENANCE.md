# Figure Provenance

## Figure 2

Model: Meta-Llama-3.1-8B
Hardware: RTX Pro 4500 (Blackwell)
Task: Happy -> Computer
alpha: 15
temperature: 0.8
seed: 42
Grid: 41 x 19 = 779
Source:
data/sweep_computer_llama8b_a15.jsonl

## Figure 4

Model: Meta-Llama-3.1-8B
Hardware A: RTX Pro 4500 (Blackwell)
Hardware B: RTX 3090 (Ampere)
Task: Happy -> Computer
alpha: 15
temperature: 0.8
seed: 42
Divergent coordinates: 146 / 779

## Figure 5

Model: Meta-Llama-3.1-70B
Quantization: NF4 4-bit
Hardware: RTX Pro 4500 + RTX 3090
Task: Happy -> Computer
alpha: 30
temperature: 0.8
seed: 42
Grid: 41 x 19 = 779
source:
data/sweep_computer_llama70b_a30.jsonl

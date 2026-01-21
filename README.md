# ABM-ACE: Resilience, Inequality, and Adaptation in Economic Networks

ABM-ACE is a compact but **serious** agent-based modeling (ABM) and agent-computational economics (ACE) project that explores how **households, firms, and policy** jointly shape resilience and inequality after climate and macroeconomic shocks.

The model focuses on a socially meaningful question: **How do policies and market adaptation affect household welfare and inequality when firms face climate-related productivity shocks?** It is designed to be transparent, rigorous, and extensible so researchers and students can audit the mechanics and expand them into larger empirical or policy applications.

## Why this project matters

Climate-driven disruptions and economic volatility are deeply intertwined. Traditional representative-agent models often hide distributional impacts; ABM/ACE lets us explicitly capture **heterogeneous households**, **adaptive firms**, and **policy interventions** to understand **who gains, who loses, and how resilience emerges (or fails)**.

## Model overview (high level)

**Agents**
- **Households**: heterogeneous wealth, income, consumption needs, and risk tolerance.
- **Firms**: adapt wages and hiring based on productivity, demand, and climate shocks.
- **Policy**: a simple carbon tax + dividend policy (recycling revenue to households) to examine distributional impacts.

**Key dynamics**
- Climate shocks reduce firm productivity.
- Firms adapt wages and hiring to maintain viability.
- Households adjust consumption and savings under uncertainty.
- A carbon tax internalizes emissions and redistributes revenue.

**Outcomes tracked**
- Inequality (Gini coefficient)
- Unemployment
- Average real consumption
- Firm survival rates
- Aggregate emissions

## Getting started

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Run a demo simulation
```bash
abm-ace --steps 60 --seed 7
```

### Run the script directly
```bash
python scripts/run_demo.py
```

## Repository layout

```
.
├── src/abm_ace
│   ├── cli.py          # command-line interface
│   ├── metrics.py      # inequality & summary metrics
│   ├── model.py        # core simulation model
│   └── types.py        # dataclasses for households/firms/policy
├── scripts
│   └── run_demo.py     # one-shot demo
├── TODO.md
└── README.md
```

## Example output (truncated)
```
step=0 households=200 firms=30 gini=0.32 unemployment=0.08 avg_consumption=1.01 emissions=0.94
...
step=59 households=200 firms=30 gini=0.41 unemployment=0.13 avg_consumption=0.97 emissions=0.71
```

## Design principles

- **Clarity**: simple, readable code paths with transparent assumptions.
- **Accountability**: metrics and policy levers are explicit and auditable.
- **Rigor**: deterministic reproducibility via RNG seeds.
- **Extensibility**: modular agents and metrics to support expansion.

## Roadmap
See [TODO.md](TODO.md) for near-term enhancements.

## Citation
If this repository helps your research or teaching, please cite it as:
```
ABM-ACE: Resilience, Inequality, and Adaptation in Economic Networks. (2024).
```

## License
MIT

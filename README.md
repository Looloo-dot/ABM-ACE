# ABM-ACE: Adaptive Agents, Socio-Economic Resilience & Climate Equity

**ABM-ACE** is an agent-based modeling (ABM) research sandbox for **computational
economics** and **computational social science**. It explores how *adaptive,
boundedly rational agents* interact in a **policy-relevant** environment where
**climate shocks**, **inequality**, and **social influence** co-evolve. The project
is designed to be **intermediate/advanced**, **innovative**, and **socially
meaningful**, with clear documentation and reproducible experiments.

---

## Project Vision

We model a stylized economy where households and firms face:

- **Climate shocks** that reduce productivity and damage assets.
- **Endogenous inequality** due to heterogeneous skills, network access, and adaptation capacity.
- **Policy levers** (e.g., green subsidies, progressive taxation, targeted transfers).
- **Social influence** that spreads adaptation behavior and low-carbon norms.

The goal is not a single “answer,” but a **transparent computational laboratory** for evaluating how *micro-level adaptation rules* shape *macro-level outcomes* such as inequality, resilience, and emissions.

---

## Model Summary

**Agents**
- **Households**: supply labor, consume, adapt to climate risk, invest in green tech.
- **Firms**: hire labor, produce output, decide on green upgrades.

**Key mechanisms**
- Climate shocks reduce productivity and impose asset losses.
- Social networks diffuse adaptive behavior.
- Policies influence investment choices and redistribute risk.

**Core outcomes**
- Wealth distribution (Gini, top shares)
- Emissions / green adoption rate
- Resilience (speed of recovery after shocks)

---

## Repository Structure

```
.
├── README.md
├── TODO.md
├── pyproject.toml
├── requirements.txt
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── src
    └── abm_ace
        ├── __init__.py
        ├── agents.py
        ├── model.py
        ├── metrics.py
        └── run.py
```

---

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m abm_ace.run --steps 200 --seed 42
```

The script will output a CSV summary, a run configuration snapshot, and a quick
plot of system-level outcomes.

---

## Configuration & Reproducibility

The CLI exposes all model and policy parameters so that every run is
reproducible and auditable. Use `--output` to set a dedicated results folder; a
`run_config.json` file is automatically saved alongside the metrics.

Example:

```bash
python -m abm_ace.run \
  --steps 300 \
  --seed 7 \
  --green-subsidy 0.3 \
  --progressive-tax 0.2 \
  --targeted-transfer 0.15 \
  --output outputs/experiment_001
```

---

## Research Questions

- Under what conditions do adaptation subsidies reduce inequality *and* emissions?
- Does social influence accelerate green adoption or reinforce inequality?
- How resilient are different policy regimes to cascading shocks?

---

## Accountability & Transparency

This project prioritizes:

- **Clarity**: documented assumptions and readable code.
- **Rigor**: explicit metrics and reproducible runs.
- **Transparency**: no hidden parameters; all configuration is declared.
- **Accountability**: design decisions and limitations are recorded in TODO.md.

---

## Next Steps

See [TODO.md](TODO.md) for structured research and engineering tasks.

---

## License

MIT (see [LICENSE](LICENSE)).

---

## Contributing & Community

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.

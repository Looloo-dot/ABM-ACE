from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from abm_ace.model import ABMModel, ModelConfig, Policy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ABM-ACE simulation.")
    parser.add_argument("--steps", type=int, default=200, help="Number of steps")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=Path, default=Path("outputs"), help="Output dir")

    parser.add_argument("--num-households", type=int, default=200)
    parser.add_argument("--num-firms", type=int, default=40)
    parser.add_argument("--shock-probability", type=float, default=0.1)
    parser.add_argument("--shock-severity", type=float, default=0.4)
    parser.add_argument("--network-rewire-prob", type=float, default=0.02)

    parser.add_argument("--green-subsidy", type=float, default=0.25)
    parser.add_argument("--progressive-tax", type=float, default=0.15)
    parser.add_argument("--targeted-transfer", type=float, default=0.1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    config = ModelConfig(
        num_households=args.num_households,
        num_firms=args.num_firms,
        shock_probability=args.shock_probability,
        shock_severity=args.shock_severity,
        network_rewire_prob=args.network_rewire_prob,
    )
    policy = Policy(
        green_subsidy=args.green_subsidy,
        progressive_tax=args.progressive_tax,
        targeted_transfer=args.targeted_transfer,
    )

    run_config = {
        "steps": args.steps,
        "seed": args.seed,
        "model_config": asdict(config),
        "policy": asdict(policy),
    }

    model = ABMModel(config=config, policy=policy, seed=args.seed)
    metrics = model.run(args.steps)

    df = pd.DataFrame([m.__dict__ for m in metrics])
    output_csv = args.output / "metrics.csv"
    df.to_csv(output_csv, index=False)

    config_path = args.output / "run_config.json"
    config_path.write_text(json.dumps(run_config, indent=2))

    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    df.plot(x="step", y="avg_wealth", ax=axes[0, 0], title="Average Wealth")
    df.plot(x="step", y="gini", ax=axes[0, 1], title="Inequality (Gini)")
    df.plot(x="step", y="green_adoption", ax=axes[1, 0], title="Green Adoption")
    df.plot(x="step", y="emissions", ax=axes[1, 1], title="Emissions Intensity")
    fig.tight_layout()
    fig_path = args.output / "summary.png"
    fig.savefig(fig_path, dpi=150)

    print(f"Saved metrics to {output_csv}")
    print(f"Saved run config to {config_path}")
    print(f"Saved plot to {fig_path}")


if __name__ == "__main__":
    main()

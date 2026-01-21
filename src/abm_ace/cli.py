from __future__ import annotations

import argparse

import numpy as np

from abm_ace.model import build_economy, model_config_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the ABM-ACE simulation.")
    parser.add_argument("--steps", type=int, default=60, help="Number of simulation steps.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--households", type=int, default=200, help="Number of household agents.")
    parser.add_argument("--firms", type=int, default=30, help="Number of firm agents.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    economy = build_economy(rng, households=args.households, firms=args.firms)
    summary = model_config_summary(economy)
    print(f"config={summary}")

    for _ in range(args.steps):
        metrics = economy.step()
        print(
            "step={step:.0f} households={households:.0f} firms={firms:.0f} "
            "gini={gini:.2f} unemployment={unemployment:.2f} "
            "avg_income={avg_income:.2f} emissions={emissions:.2f}".format(**metrics)
        )


if __name__ == "__main__":
    main()

from __future__ import annotations

import numpy as np

from abm_ace.model import build_economy


def main() -> None:
    rng = np.random.default_rng(7)
    economy = build_economy(rng)
    for _ in range(30):
        metrics = economy.step()
        print(metrics)


if __name__ == "__main__":
    main()

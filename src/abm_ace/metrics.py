from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Metrics:
    """Container for model-wide metrics at each step."""

    step: int
    avg_wealth: float
    gini: float
    green_adoption: float
    emissions: float
    resilience: float


def gini_coefficient(values: np.ndarray) -> float:
    """Compute the Gini coefficient for a 1D array of values."""
    if np.allclose(values, 0):
        return 0.0
    sorted_values = np.sort(values)
    n = len(values)
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * sorted_values) / (n * np.sum(sorted_values))) - (n + 1) / n)


def resilience_index(output_history: List[float]) -> float:
    """Measure resilience as recovery speed after a shock."""
    if len(output_history) < 3:
        return 0.0
    peak = max(output_history)
    last = output_history[-1]
    return float(np.clip(last / peak, 0.0, 1.0))

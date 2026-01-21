from __future__ import annotations

from typing import Iterable


def gini(values: Iterable[float]) -> float:
    sorted_vals = sorted(v for v in values if v >= 0)
    if not sorted_vals:
        return 0.0
    total = sum(sorted_vals)
    if total == 0:
        return 0.0
    cumulative = 0.0
    weighted = 0.0
    for idx, value in enumerate(sorted_vals, start=1):
        cumulative += value
        weighted += cumulative
    n = len(sorted_vals)
    return (n + 1 - 2 * weighted / total) / n

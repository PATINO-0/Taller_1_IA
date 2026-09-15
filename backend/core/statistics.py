from statistics import mean
from typing import Any


def summarize_numeric(
    values: list[float],
) -> dict[str, float]:
    """Calcula mínimo, máximo y promedio."""

    if not values:
        return {
            "best": 0.0,
            "worst": 0.0,
            "average": 0.0,
        }

    return {
        "best": min(values),
        "worst": max(values),
        "average": mean(values),
    }


def summarize_runs(
    runs: list[dict[str, Any]],
    metric: str,
    minimize: bool = True,
) -> dict[str, float]:
    """Resume una métrica de varias corridas."""

    values = [
        float(run[metric])
        for run in runs
    ]

    if not values:
        return {
            "best": 0.0,
            "worst": 0.0,
            "average": 0.0,
        }

    best = (
        min(values)
        if minimize
        else max(values)
    )

    worst = (
        max(values)
        if minimize
        else min(values)
    )

    return {
        "best": best,
        "worst": worst,
        "average": mean(values),
    }

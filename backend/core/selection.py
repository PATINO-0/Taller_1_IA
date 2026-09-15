import random

from collections.abc import Callable, Sequence
from typing import TypeVar


T = TypeVar("T")


def tournament_select(
    population: Sequence[T],
    score_function: Callable[[T], float],
    rng: random.Random,
    tournament_size: int = 3,
    maximize: bool = False,
) -> T:
    """Selecciona un individuo mediante torneo."""

    size = min(
        tournament_size,
        len(population),
    )

    contenders = rng.sample(
        list(population),
        size,
    )

    return (max if maximize else min)(
        contenders,
        key=score_function,
    )

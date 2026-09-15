import random


def one_point_crossover(
    parent_a: list[int],
    parent_b: list[int],
    rng: random.Random,
) -> tuple[list[int], list[int]]:
    """Cruce de un punto para cromosomas binarios."""

    if len(parent_a) < 2:
        return (
            parent_a.copy(),
            parent_b.copy(),
        )

    point = rng.randint(
        1,
        len(parent_a) - 1,
    )

    child_a = (
        parent_a[:point]
        + parent_b[point:]
    )

    child_b = (
        parent_b[:point]
        + parent_a[point:]
    )

    return child_a, child_b


def bit_flip_mutation(
    individual: list[int],
    mutation_rate: float,
    rng: random.Random,
) -> list[int]:
    """Invierte cada bit con una probabilidad."""

    return [
        (
            1 - gene
            if rng.random() < mutation_rate
            else gene
        )
        for gene in individual
    ]

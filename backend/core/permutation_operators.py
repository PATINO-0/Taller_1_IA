import random


def order_crossover(
    parent_a: list[int],
    parent_b: list[int],
    rng: random.Random,
) -> tuple[list[int], list[int]]:
    """Cruce OX que conserva permutaciones válidas."""

    size = len(parent_a)

    left, right = sorted(
        rng.sample(
            range(size),
            2,
        )
    )

    def build_child(
        first: list[int],
        second: list[int],
    ) -> list[int]:
        child: list[int | None] = [None] * size

        child[left:right + 1] = first[
            left:right + 1
        ]

        remaining = [
            gene
            for gene in second
            if gene not in child
        ]

        remaining_index = 0

        indexes = (
            list(range(right + 1, size))
            + list(range(0, left))
        )

        for index in indexes:
            child[index] = remaining[
                remaining_index
            ]
            remaining_index += 1

        return [
            int(gene)
            for gene in child
        ]

    child_a = build_child(
        parent_a,
        parent_b,
    )

    child_b = build_child(
        parent_b,
        parent_a,
    )

    return child_a, child_b


def swap_mutation(
    individual: list[int],
    rng: random.Random,
) -> list[int]:
    """Intercambia dos posiciones."""

    mutated = individual.copy()

    first, second = rng.sample(
        range(len(mutated)),
        2,
    )

    mutated[first], mutated[second] = (
        mutated[second],
        mutated[first],
    )

    return mutated


def inversion_mutation(
    individual: list[int],
    rng: random.Random,
) -> list[int]:
    """Invierte un segmento de la permutación."""

    mutated = individual.copy()

    left, right = sorted(
        rng.sample(
            range(len(mutated)),
            2,
        )
    )

    mutated[left:right + 1] = reversed(
        mutated[left:right + 1]
    )

    return mutated

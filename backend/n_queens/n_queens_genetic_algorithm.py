import random

from backend.core.evolution_result import EvolutionResult
from backend.core.genetic_algorithm_config import (
    GeneticAlgorithmConfig,
)
from backend.core.permutation_operators import (
    order_crossover,
    swap_mutation,
)
from backend.core.selection import tournament_select


class NQueensGeneticAlgorithm:
    """Algoritmo genético para N-Reinas."""

    def __init__(
        self,
        n: int,
        config: GeneticAlgorithmConfig,
    ) -> None:
        self.n = n
        self.config = config
        self.rng = random.Random(
            config.seed
        )

    def _create_individual(
        self,
    ) -> list[int]:
        individual = list(
            range(self.n)
        )

        self.rng.shuffle(
            individual
        )

        return individual

    def _create_population(
        self,
    ) -> list[list[int]]:
        return [
            self._create_individual()
            for _ in range(
                self.config.population_size
            )
        ]

    def conflicts(
        self,
        individual: list[int],
    ) -> int:
        """Cuenta pares de reinas que se atacan."""

        conflicts = 0

        for first_column in range(
            self.n
        ):
            for second_column in range(
                first_column + 1,
                self.n,
            ):
                same_row = (
                    individual[first_column]
                    == individual[second_column]
                )

                same_diagonal = (
                    abs(
                        individual[first_column]
                        - individual[second_column]
                    )
                    == abs(
                        first_column
                        - second_column
                    )
                )

                if (
                    same_row
                    or same_diagonal
                ):
                    conflicts += 1

        return conflicts

    def run(
        self,
    ) -> EvolutionResult:
        population = (
            self._create_population()
        )

        history: list[
            dict[str, float]
        ] = []

        for generation in range(
            self.config.max_generations + 1
        ):
            population.sort(
                key=self.conflicts
            )

            best = population[0]

            best_conflicts = (
                self.conflicts(best)
            )

            average_conflicts = (
                sum(
                    self.conflicts(item)
                    for item in population
                )
                / len(population)
            )

            history.append(
                {
                    "generation": float(
                        generation
                    ),
                    "best": float(
                        best_conflicts
                    ),
                    "average": float(
                        average_conflicts
                    ),
                }
            )

            if best_conflicts == 0:
                return EvolutionResult(
                    best_individual=(
                        best.copy()
                    ),
                    best_score=0.0,
                    generation=generation,
                    solved=True,
                    history=history,
                    metadata={
                        "n": self.n
                    },
                )

            elite_count = min(
                self.config.elitism_count,
                len(population),
            )

            next_population = [
                individual.copy()
                for individual
                in population[:elite_count]
            ]

            while (
                len(next_population)
                < self.config.population_size
            ):
                parent_a = tournament_select(
                    population,
                    self.conflicts,
                    self.rng,
                    self.config.tournament_size,
                    maximize=False,
                )

                parent_b = tournament_select(
                    population,
                    self.conflicts,
                    self.rng,
                    self.config.tournament_size,
                    maximize=False,
                )

                child_a, child_b = (
                    order_crossover(
                        parent_a,
                        parent_b,
                        self.rng,
                    )
                )

                if (
                    self.rng.random()
                    < self.config.mutation_rate
                ):
                    child_a = (
                        swap_mutation(
                            child_a,
                            self.rng,
                        )
                    )

                if (
                    self.rng.random()
                    < self.config.mutation_rate
                ):
                    child_b = (
                        swap_mutation(
                            child_b,
                            self.rng,
                        )
                    )

                next_population.append(
                    child_a
                )

                if (
                    len(next_population)
                    < self.config.population_size
                ):
                    next_population.append(
                        child_b
                    )

            population = next_population

        population.sort(
            key=self.conflicts
        )

        best = population[0]

        return EvolutionResult(
            best_individual=best.copy(),
            best_score=float(
                self.conflicts(best)
            ),
            generation=(
                self.config.max_generations
            ),
            solved=(
                self.conflicts(best) == 0
            ),
            history=history,
            metadata={
                "n": self.n
            },
        )


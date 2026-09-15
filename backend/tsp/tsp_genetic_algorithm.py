import random

from backend.core.evolution_result import EvolutionResult
from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.core.permutation_operators import (
    inversion_mutation,
    order_crossover,
    swap_mutation,
)
from backend.core.selection import tournament_select
from backend.tsp.tsp_dataset import TSPDataset


class TSPGeneticAlgorithm:
    """Algoritmo genético para TSP."""

    def __init__(
        self,
        dataset: TSPDataset,
        config: GeneticAlgorithmConfig,
        mutation_strategy: str = "inversion",
    ) -> None:
        self.dataset = dataset
        self.config = config
        self.mutation_strategy = mutation_strategy
        self.rng = random.Random(config.seed)

    def _create_individual(self) -> list[int]:
        route = list(range(self.dataset.city_count))
        self.rng.shuffle(route)
        return route

    def _create_population(self) -> list[list[int]]:
        return [
            self._create_individual()
            for _ in range(self.config.population_size)
        ]

    def _mutate(self, individual: list[int]) -> list[int]:
        if self.mutation_strategy == "swap":
            return swap_mutation(individual, self.rng)

        return inversion_mutation(individual, self.rng)

    def run(self) -> EvolutionResult:
        population = self._create_population()
        history: list[dict[str, float]] = []
        global_best: list[int] | None = None
        global_best_distance = float("inf")
        best_generation = 0
        stagnant_generations = 0

        for generation in range(self.config.max_generations + 1):
            population.sort(key=self.dataset.route_distance)
            best = population[0]
            best_distance = self.dataset.route_distance(best)
            average_distance = (
                sum(
                    self.dataset.route_distance(route)
                    for route in population
                )
                / len(population)
            )

            if best_distance + 1e-9 < global_best_distance:
                global_best = best.copy()
                global_best_distance = best_distance
                best_generation = generation
                stagnant_generations = 0
            else:
                stagnant_generations += 1

            history.append(
                {
                    "generation": float(generation),
                    "best": round(global_best_distance, 3),
                    "average": round(average_distance, 3),
                }
            )

            # Detiene la búsqueda si deja de mejorar.
            if stagnant_generations >= 250:
                break

            elite_count = min(
                self.config.elitism_count,
                len(population),
            )
            next_population = [
                route.copy()
                for route in population[:elite_count]
            ]

            while len(next_population) < self.config.population_size:
                parent_a = tournament_select(
                    population,
                    self.dataset.route_distance,
                    self.rng,
                    self.config.tournament_size,
                    maximize=False,
                )
                parent_b = tournament_select(
                    population,
                    self.dataset.route_distance,
                    self.rng,
                    self.config.tournament_size,
                    maximize=False,
                )
                child_a, child_b = order_crossover(
                    parent_a,
                    parent_b,
                    self.rng,
                )

                if self.rng.random() < self.config.mutation_rate:
                    child_a = self._mutate(child_a)

                if self.rng.random() < self.config.mutation_rate:
                    child_b = self._mutate(child_b)

                next_population.append(child_a)

                if len(next_population) < self.config.population_size:
                    next_population.append(child_b)

            population = next_population

        assert global_best is not None

        return EvolutionResult(
            best_individual=global_best,
            best_score=round(global_best_distance, 3),
            generation=best_generation,
            solved=True,
            history=history,
            metadata={
                "city_count": self.dataset.city_count,
                "mutation_strategy": self.mutation_strategy,
                "executed_generations": len(history) - 1,
            },
        )


import random

from backend.core.binary_operators import bit_flip_mutation, one_point_crossover
from backend.core.evolution_result import EvolutionResult
from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.core.selection import tournament_select
from backend.knapsack.knapsack_dataset import KnapsackDataset


class KnapsackGeneticAlgorithm:
    """Algoritmo genético binario para mochila."""

    def __init__(
        self,
        dataset: KnapsackDataset,
        capacity: int,
        config: GeneticAlgorithmConfig,
        constraint_strategy: str = "repair",
    ) -> None:
        self.dataset = dataset
        self.capacity = capacity
        self.config = config
        self.constraint_strategy = constraint_strategy
        self.rng = random.Random(config.seed)

    def _create_individual(self) -> list[int]:
        individual = [
            self.rng.randint(0, 1)
            for _ in self.dataset.items
        ]

        if self.constraint_strategy == "repair":
            return self._repair(individual)

        return individual

    def _create_population(self) -> list[list[int]]:
        return [
            self._create_individual()
            for _ in range(self.config.population_size)
        ]

    def totals(self, individual: list[int]) -> tuple[int, int]:
        weight = sum(
            gene * item.weight
            for gene, item in zip(
                individual,
                self.dataset.items,
                strict=True,
            )
        )
        value = sum(
            gene * item.value
            for gene, item in zip(
                individual,
                self.dataset.items,
                strict=True,
            )
        )
        return weight, value

    def fitness(self, individual: list[int]) -> float:
        weight, value = self.totals(individual)

        if weight <= self.capacity:
            return float(value)

        excess = weight - self.capacity

        # Una solución inválida pierde aptitud.
        return max(0.0, float(value - excess * 100))

    def _repair(self, individual: list[int]) -> list[int]:
        repaired = individual.copy()
        weight, _ = self.totals(repaired)

        while weight > self.capacity:
            selected_indexes = [
                index
                for index, gene in enumerate(repaired)
                if gene == 1
            ]

            if not selected_indexes:
                break

            # Retira el objeto con peor valor/peso.
            worst_index = min(
                selected_indexes,
                key=lambda index: (
                    self.dataset.items[index].value
                    / self.dataset.items[index].weight
                ),
            )
            repaired[worst_index] = 0
            weight, _ = self.totals(repaired)

        return repaired

    def run(self) -> EvolutionResult:
        population = self._create_population()
        history: list[dict[str, float]] = []
        global_best: list[int] | None = None
        global_best_fitness = float("-inf")
        best_generation = 0
        stagnation = 0

        for generation in range(self.config.max_generations + 1):
            population.sort(key=self.fitness, reverse=True)
            best = population[0]
            best_fitness = self.fitness(best)
            average_fitness = (
                sum(self.fitness(item) for item in population)
                / len(population)
            )

            if best_fitness > global_best_fitness + 1e-9:
                global_best = best.copy()
                global_best_fitness = best_fitness
                best_generation = generation
                stagnation = 0
            else:
                stagnation += 1

            history.append(
                {
                    "generation": float(generation),
                    "best": round(global_best_fitness, 3),
                    "average": round(average_fitness, 3),
                }
            )

            if stagnation >= 120:
                break

            elite_count = min(
                self.config.elitism_count,
                len(population),
            )
            next_population = [
                item.copy()
                for item in population[:elite_count]
            ]

            while len(next_population) < self.config.population_size:
                parent_a = tournament_select(
                    population,
                    self.fitness,
                    self.rng,
                    self.config.tournament_size,
                    maximize=True,
                )
                parent_b = tournament_select(
                    population,
                    self.fitness,
                    self.rng,
                    self.config.tournament_size,
                    maximize=True,
                )
                child_a, child_b = one_point_crossover(
                    parent_a,
                    parent_b,
                    self.rng,
                )
                child_a = bit_flip_mutation(
                    child_a,
                    self.config.mutation_rate,
                    self.rng,
                )
                child_b = bit_flip_mutation(
                    child_b,
                    self.config.mutation_rate,
                    self.rng,
                )

                if self.constraint_strategy == "repair":
                    child_a = self._repair(child_a)
                    child_b = self._repair(child_b)

                next_population.append(child_a)

                if len(next_population) < self.config.population_size:
                    next_population.append(child_b)

            population = next_population

        assert global_best is not None
        weight, value = self.totals(global_best)
        return EvolutionResult(
            best_individual=global_best,
            best_score=float(value),
            generation=best_generation,
            solved=weight <= self.capacity,
            history=history,
            metadata={
                "weight": weight,
                "value": value,
                "capacity": self.capacity,
                "constraint_strategy": self.constraint_strategy,
                "fitness": self.fitness(global_best),
                "executed_generations": len(history) - 1,
            },
        )


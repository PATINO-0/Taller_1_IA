from statistics import mean

from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.knapsack.knapsack_dataset import KnapsackDataset
from backend.knapsack.knapsack_genetic_algorithm import (
    KnapsackGeneticAlgorithm,
)
from backend.schemas.knapsack_experiment_request import (
    KnapsackExperimentRequest,
)
from backend.schemas.knapsack_request import KnapsackRequest


class KnapsackService:
    """Gestiona las operaciones de mochila."""

    def _exact_solution(
        self,
        dataset: KnapsackDataset,
        capacity: int,
    ) -> dict:
        """Calcula referencia exacta con programación dinámica."""

        item_count = len(dataset.items)
        dp = [
            [0] * (capacity + 1)
            for _ in range(item_count + 1)
        ]

        for item_index in range(1, item_count + 1):
            item = dataset.items[item_index - 1]

            for current_capacity in range(capacity + 1):
                dp[item_index][current_capacity] = dp[item_index - 1][
                    current_capacity
                ]

                if item.weight <= current_capacity:
                    with_item = (
                        item.value
                        + dp[item_index - 1][current_capacity - item.weight]
                    )
                    dp[item_index][current_capacity] = max(
                        dp[item_index][current_capacity],
                        with_item,
                    )

        chromosome = [0] * item_count
        current_capacity = capacity

        for item_index in range(item_count, 0, -1):
            current_value = dp[item_index][current_capacity]
            previous_value = dp[item_index - 1][current_capacity]

            if current_value != previous_value:
                chromosome[item_index - 1] = 1
                current_capacity -= dataset.items[item_index - 1].weight

        weight = sum(
            gene * item.weight
            for gene, item in zip(
                chromosome,
                dataset.items,
                strict=True,
            )
        )
        return {
            "value": dp[item_count][capacity],
            "weight": weight,
            "chromosome": chromosome,
        }

    def _serialize_items(self, dataset: KnapsackDataset) -> list[dict]:
        return [
            {
                "name": item.name,
                "weight": item.weight,
                "value": item.value,
            }
            for item in dataset.items
        ]

    def run(self, request: KnapsackRequest) -> dict:
        dataset = KnapsackDataset()
        config = GeneticAlgorithmConfig(
            population_size=request.population_size,
            mutation_rate=request.mutation_rate,
            max_generations=request.max_generations,
            elitism_count=min(
                request.elitism_count,
                request.population_size,
            ),
            seed=request.seed,
        )
        algorithm = KnapsackGeneticAlgorithm(
            dataset,
            request.capacity,
            config,
            request.constraint_strategy,
        )
        result = algorithm.run().to_dict()
        weight = result["metadata"]["weight"]
        value = result["metadata"]["value"]
        result["weight"] = weight
        result["value"] = value
        result["selected_items"] = [
            item.name
            for gene, item in zip(
                result["best_individual"],
                dataset.items,
                strict=True,
            )
            if gene == 1
        ]
        result["items"] = self._serialize_items(dataset)
        exact = self._exact_solution(dataset, request.capacity)
        result["exact_reference"] = exact
        result["optimality_gap"] = exact["value"] - value
        result["parameters"] = request.model_dump()
        return result

    def experiment(self, request: KnapsackExperimentRequest) -> dict:
        dataset = KnapsackDataset()
        rows: list[dict] = []

        for capacity in request.capacities:
            exact = self._exact_solution(dataset, capacity)

            for strategy in request.strategies:
                if strategy not in {"penalty", "repair"}:
                    raise ValueError(
                        "Las estrategias válidas son penalty y repair."
                    )

                run_results: list[dict] = []

                for run_index in range(request.runs):
                    config = GeneticAlgorithmConfig(
                        population_size=request.population_size,
                        mutation_rate=request.mutation_rate,
                        max_generations=request.max_generations,
                        elitism_count=2,
                        seed=40_000 + capacity * 100 + run_index,
                    )
                    result = KnapsackGeneticAlgorithm(
                        dataset,
                        capacity,
                        config,
                        strategy,
                    ).run()
                    run_results.append(
                        {
                            "value": result.metadata["value"],
                            "weight": result.metadata["weight"],
                            "generation": result.generation,
                            "valid": result.solved,
                        }
                    )

                feasible = [run for run in run_results if run["valid"]]
                values = [run["value"] for run in feasible] or [0]
                rows.append(
                    {
                        "capacity": capacity,
                        "strategy": strategy,
                        "runs": request.runs,
                        "valid_rate": len(feasible) / request.runs,
                        "best_value": max(values),
                        "worst_value": min(values),
                        "average_value": round(mean(values), 2),
                        "average_weight": (
                            round(
                                mean(run["weight"] for run in feasible),
                                2,
                            )
                            if feasible
                            else None
                        ),
                        "average_best_generation": round(
                            mean(run["generation"] for run in run_results),
                            2,
                        ),
                        "exact_optimum": exact["value"],
                        "average_gap": round(
                            exact["value"] - mean(values),
                            2,
                        ),
                    }
                )

        return {
            "rows": rows,
            "items": self._serialize_items(dataset),
        }


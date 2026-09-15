from statistics import mean

from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.n_queens.n_queens_genetic_algorithm import NQueensGeneticAlgorithm
from backend.schemas.n_queens_experiment_request import NQueensExperimentRequest
from backend.schemas.n_queens_request import NQueensRequest


class NQueensService:
    """Gestiona corridas y experimentos."""

    def run(self, request: NQueensRequest) -> dict:
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

        algorithm = NQueensGeneticAlgorithm(request.n, config)
        result = algorithm.run().to_dict()
        result["conflicts"] = int(result["best_score"])
        result["parameters"] = request.model_dump()
        return result

    def experiment(self, request: NQueensExperimentRequest) -> dict:
        rows: list[dict] = []

        for n in request.n_values:
            for population_size in request.population_sizes:
                for mutation_rate in request.mutation_rates:
                    generations: list[int] = []
                    conflicts: list[int] = []
                    successful_generations: list[int] = []

                    for run_index in range(request.runs):
                        config = GeneticAlgorithmConfig(
                            population_size=population_size,
                            mutation_rate=mutation_rate,
                            max_generations=request.max_generations,
                            elitism_count=2,
                            seed=(
                                10_000
                                + n * 1000
                                + population_size * 10
                                + run_index
                            ),
                        )
                        result = NQueensGeneticAlgorithm(n, config).run()
                        generations.append(result.generation)
                        conflicts.append(int(result.best_score))

                        if result.solved:
                            successful_generations.append(result.generation)

                    rows.append(
                        {
                            "n": n,
                            "population_size": population_size,
                            "mutation_rate": mutation_rate,
                            "runs": request.runs,
                            "success_rate": (
                                len(successful_generations) / request.runs
                            ),
                            "best_generation": (
                                min(successful_generations)
                                if successful_generations
                                else None
                            ),
                            "worst_generation": (
                                max(successful_generations)
                                if successful_generations
                                else None
                            ),
                            "average_generation": (
                                mean(successful_generations)
                                if successful_generations
                                else None
                            ),
                            "average_final_conflicts": mean(conflicts),
                            "average_executed_generations": mean(generations),
                        }
                    )

        return {
            "rows": rows,
            "runs_per_configuration": request.runs,
        }


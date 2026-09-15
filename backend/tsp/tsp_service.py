from statistics import mean

from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.schemas.tsp_experiment_request import TSPExperimentRequest
from backend.schemas.tsp_request import TSPRequest
from backend.tsp.tsp_dataset import TSPDataset
from backend.tsp.tsp_genetic_algorithm import TSPGeneticAlgorithm


class TSPService:
    """Gestiona corridas y experimentos TSP."""

    def run(self, request: TSPRequest) -> dict:
        dataset = TSPDataset(request.city_count)
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
        algorithm = TSPGeneticAlgorithm(
            dataset,
            config,
            request.mutation_strategy,
        )
        result = algorithm.run().to_dict()
        result["distance"] = result["best_score"]
        result["route"] = (
            result["best_individual"]
            + [result["best_individual"][0]]
        )
        result["coordinates"] = dataset.coordinates
        result["distance_matrix"] = dataset.distance_matrix
        result["parameters"] = request.model_dump()
        return result

    def experiment(self, request: TSPExperimentRequest) -> dict:
        dataset = TSPDataset(request.city_count)
        rows: list[dict] = []

        for strategy in request.mutation_strategies:
            for mutation_rate in request.mutation_rates:
                runs: list[dict] = []

                for run_index in range(request.runs):
                    config = GeneticAlgorithmConfig(
                        population_size=request.population_size,
                        mutation_rate=mutation_rate,
                        max_generations=request.max_generations,
                        elitism_count=2,
                        seed=(
                            20_000
                            + run_index
                            + int(mutation_rate * 1000)
                        ),
                    )
                    result = TSPGeneticAlgorithm(
                        dataset,
                        config,
                        strategy,
                    ).run()
                    runs.append(
                        {
                            "distance": result.best_score,
                            "generation": result.generation,
                            "route": result.best_individual,
                        }
                    )

                distances = [float(run["distance"]) for run in runs]
                generations = [int(run["generation"]) for run in runs]
                best_run = min(runs, key=lambda item: item["distance"])
                rows.append(
                    {
                        "mutation_strategy": strategy,
                        "mutation_rate": mutation_rate,
                        "runs": request.runs,
                        "best_distance": min(distances),
                        "worst_distance": max(distances),
                        "average_distance": round(mean(distances), 3),
                        "average_best_generation": round(
                            mean(generations),
                            2,
                        ),
                        "best_route": (
                            best_run["route"] + [best_run["route"][0]]
                        ),
                    }
                )

        return {
            "city_count": request.city_count,
            "rows": rows,
            "coordinates": dataset.coordinates,
        }


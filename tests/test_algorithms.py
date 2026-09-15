from backend.core.genetic_algorithm_config import (
    GeneticAlgorithmConfig,
)
from backend.knapsack.knapsack_dataset import (
    KnapsackDataset,
)
from backend.knapsack.knapsack_genetic_algorithm import (
    KnapsackGeneticAlgorithm,
)
from backend.n_queens.n_queens_genetic_algorithm import (
    NQueensGeneticAlgorithm,
)
from backend.scheduling.course_scheduling_genetic_algorithm import (
    CourseSchedulingGeneticAlgorithm,
)
from backend.scheduling.scheduling_dataset import (
    SchedulingDataset,
)
from backend.tsp.tsp_dataset import (
    TSPDataset,
)
from backend.tsp.tsp_genetic_algorithm import (
    TSPGeneticAlgorithm,
)


def test_n_queens_finds_zero_conflicts() -> None:
    config = GeneticAlgorithmConfig(
        population_size=100,
        mutation_rate=0.1,
        max_generations=1000,
        elitism_count=2,
        seed=7,
    )

    result = (
        NQueensGeneticAlgorithm(
            8,
            config,
        ).run()
    )

    assert (
        result.best_score
        == 0
    )

    assert result.solved


def test_tsp_keeps_valid_permutation() -> None:
    dataset = TSPDataset(8)

    config = GeneticAlgorithmConfig(
        population_size=60,
        mutation_rate=0.1,
        max_generations=100,
        elitism_count=2,
        seed=7,
    )

    result = (
        TSPGeneticAlgorithm(
            dataset,
            config,
            "inversion",
        ).run()
    )

    assert sorted(
        result.best_individual
    ) == list(
        range(8)
    )

    assert (
        result.best_score
        > 0
    )


def test_scheduling_can_find_valid_solution() -> None:
    dataset = (
        SchedulingDataset()
    )

    config = GeneticAlgorithmConfig(
        population_size=180,
        mutation_rate=0.12,
        max_generations=1200,
        elitism_count=3,
        seed=7,
    )

    result = (
        CourseSchedulingGeneticAlgorithm(
            dataset,
            config,
        ).run()
    )

    assert (
        result.metadata[
            "hard_penalty"
        ]
        == 0
    )

    assert result.solved


def test_knapsack_respects_capacity_with_repair() -> None:
    dataset = (
        KnapsackDataset()
    )

    config = GeneticAlgorithmConfig(
        population_size=100,
        mutation_rate=0.03,
        max_generations=400,
        elitism_count=2,
        seed=7,
    )

    result = (
        KnapsackGeneticAlgorithm(
            dataset,
            35,
            config,
            "repair",
        ).run()
    )

    assert (
        result.metadata[
            "weight"
        ]
        <= 35
    )

    assert result.solved


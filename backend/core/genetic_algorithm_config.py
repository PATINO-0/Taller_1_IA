from dataclasses import dataclass


@dataclass(frozen=True)
class GeneticAlgorithmConfig:
    """Configuración común para los algoritmos genéticos."""

    population_size: int = 100
    mutation_rate: float = 0.1
    max_generations: int = 1000
    elitism_count: int = 2
    tournament_size: int = 3
    seed: int | None = None

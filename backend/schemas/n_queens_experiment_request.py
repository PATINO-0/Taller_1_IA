from pydantic import BaseModel, Field


class NQueensExperimentRequest(BaseModel):
    runs: int = Field(
        default=10,
        ge=2,
        le=50,
    )

    population_sizes: list[int] = Field(
        default=[30, 60, 120],
        min_length=1,
    )

    mutation_rates: list[float] = Field(
        default=[0.05, 0.1, 0.2],
        min_length=1,
    )

    n_values: list[int] = Field(
        default=[6, 8],
        min_length=1,
    )

    max_generations: int = Field(
        default=1000,
        ge=1,
        le=20000,
    )

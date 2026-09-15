from pydantic import BaseModel, Field


class KnapsackExperimentRequest(BaseModel):
    capacities: list[int] = Field(
        default=[35, 50],
        min_length=2,
        max_length=2,
    )

    strategies: list[str] = Field(
        default=[
            "penalty",
            "repair",
        ],
        min_length=2,
        max_length=2,
    )

    runs: int = Field(
        default=10,
        ge=2,
        le=50,
    )

    population_size: int = Field(
        default=120,
        ge=20,
        le=3000,
    )

    mutation_rate: float = Field(
        default=0.03,
        ge=0.0,
        le=1.0,
    )

    max_generations: int = Field(
        default=600,
        ge=1,
        le=10000,
    )


from pydantic import BaseModel, Field


class NQueensRequest(BaseModel):
    n: int = Field(
        default=8,
        ge=4,
        le=20,
    )

    population_size: int = Field(
        default=100,
        ge=10,
        le=2000,
    )

    mutation_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
    )

    max_generations: int = Field(
        default=1000,
        ge=1,
        le=20000,
    )

    elitism_count: int = Field(
        default=2,
        ge=0,
        le=50,
    )

    seed: int | None = None

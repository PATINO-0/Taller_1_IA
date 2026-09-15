from typing import Literal

from pydantic import BaseModel, Field


class TSPRequest(BaseModel):
    city_count: Literal[8, 10, 15] = 10

    population_size: int = Field(
        default=150,
        ge=20,
        le=3000,
    )

    mutation_rate: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
    )

    mutation_strategy: Literal[
        "swap",
        "inversion",
    ] = "inversion"

    max_generations: int = Field(
        default=1200,
        ge=1,
        le=20000,
    )

    elitism_count: int = Field(
        default=2,
        ge=0,
        le=50,
    )

    seed: int | None = None

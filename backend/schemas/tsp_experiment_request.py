from typing import Literal

from pydantic import BaseModel, Field


class TSPExperimentRequest(BaseModel):
    city_count: Literal[
        8,
        10,
        15,
    ] = 10

    population_size: int = Field(
        default=150,
        ge=20,
        le=3000,
    )

    mutation_rates: list[float] = Field(
        default=[0.05, 0.2],
        min_length=2,
        max_length=4,
    )

    mutation_strategies: list[
        Literal["swap", "inversion"]
    ] = Field(
        default=[
            "swap",
            "inversion",
        ],
        min_length=1,
    )

    runs: int = Field(
        default=10,
        ge=2,
        le=50,
    )

    max_generations: int = Field(
        default=1200,
        ge=1,
        le=20000,
    )

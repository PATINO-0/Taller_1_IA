from typing import Literal

from pydantic import BaseModel, Field


class KnapsackRequest(BaseModel):
    capacity: Literal[35, 50] = 35

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

    constraint_strategy: Literal[
        "penalty",
        "repair",
    ] = "repair"

    max_generations: int = Field(
        default=600,
        ge=1,
        le=10000,
    )

    elitism_count: int = Field(
        default=2,
        ge=0,
        le=50,
    )

    seed: int | None = None

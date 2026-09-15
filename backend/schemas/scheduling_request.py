from pydantic import BaseModel, Field


class SchedulingRequest(BaseModel):
    population_size: int = Field(
        default=180,
        ge=20,
        le=3000,
    )

    mutation_rate: float = Field(
        default=0.12,
        ge=0.0,
        le=1.0,
    )

    max_generations: int = Field(
        default=1500,
        ge=1,
        le=20000,
    )

    use_elitism: bool = True

    elitism_count: int = Field(
        default=3,
        ge=0,
        le=50,
    )

    seed: int | None = None

from pydantic import BaseModel, Field


class SchedulingExperimentRequest(BaseModel):
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

    runs: int = Field(
        default=10,
        ge=2,
        le=50,
    )

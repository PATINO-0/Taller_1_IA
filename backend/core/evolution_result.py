from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvolutionResult:
    """Resultado estándar de una corrida evolutiva."""

    best_individual: list[Any]
    best_score: float
    generation: int
    solved: bool

    history: list[dict[str, float]] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "best_individual": self.best_individual,
            "best_score": self.best_score,
            "generation": self.generation,
            "solved": self.solved,
            "history": self.history,
            "metadata": self.metadata,
        }

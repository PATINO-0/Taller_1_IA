from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    """Curso que debe ser programado."""

    name: str
    students: int
    required_resources: frozenset[str]
    allowed_slots: frozenset[int]


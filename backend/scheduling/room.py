from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    """Sala disponible."""

    name: str
    capacity: int
    resources: frozenset[str]
    blocked_slots: frozenset[int]


from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """Objeto candidato para la mochila."""

    name: str
    weight: int
    value: int


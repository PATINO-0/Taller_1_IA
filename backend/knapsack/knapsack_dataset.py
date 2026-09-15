from backend.knapsack.item import Item


class KnapsackDataset:
    """Datos del problema de la mochila."""

    def __init__(self) -> None:
        self.items = [
            Item("Laptop", 8, 80),
            Item("Cámara", 5, 50),
            Item("Audífonos", 2, 25),
            Item("Libro", 3, 18),
            Item("Agua", 4, 20),
            Item("Chaqueta", 6, 30),
            Item("Power bank", 2, 22),
            Item("Tablet", 5, 45),
            Item("Zapatos", 4, 28),
            Item("Botiquín", 2, 24),
            Item("Dron", 7, 65),
            Item("Linterna", 1, 12),
            Item("Alimentos", 5, 35),
            Item("Trípode", 3, 20),
            Item("GPS", 2, 27),
        ]


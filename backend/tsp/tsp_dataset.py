import math


class TSPDataset:
    """Datos de las ciudades del TSP."""

    COORDINATES = [
        (10, 10),
        (22, 35),
        (40, 18),
        (55, 42),
        (67, 12),
        (75, 33),
        (88, 18),
        (92, 52),
        (48, 68),
        (25, 72),
        (8, 58),
        (63, 84),
        (82, 75),
        (38, 90),
        (15, 88),
    ]

    def __init__(self, city_count: int) -> None:
        if city_count not in {8, 10, 15}:
            raise ValueError("city_count debe ser 8, 10 o 15.")

        self.city_count = city_count
        self.coordinates = self.COORDINATES[:city_count]
        self.distance_matrix = self._build_distance_matrix()

    def _build_distance_matrix(self) -> list[list[float]]:
        matrix: list[list[float]] = []

        for x1, y1 in self.coordinates:
            row: list[float] = []

            for x2, y2 in self.coordinates:
                distance = math.hypot(x2 - x1, y2 - y1)
                row.append(round(distance, 3))

            matrix.append(row)

        return matrix

    def route_distance(self, route: list[int]) -> float:
        total = 0.0

        for index in range(len(route)):
            current_city = route[index]
            next_city = route[(index + 1) % len(route)]
            total += self.distance_matrix[current_city][next_city]

        return total


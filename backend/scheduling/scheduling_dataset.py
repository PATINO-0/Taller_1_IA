from backend.scheduling.course import Course
from backend.scheduling.room import Room


class SchedulingDataset:
    """Datos del problema de horarios."""

    def __init__(self) -> None:
        self.slots = [
            "Lunes 08:00-10:00",
            "Lunes 10:00-12:00",
            "Martes 08:00-10:00",
            "Martes 10:00-12:00",
            "Miércoles 08:00-10:00",
        ]
        all_slots = frozenset(range(len(self.slots)))

        self.courses = [
            Course(
                "Programación I",
                28,
                frozenset({"computers", "python"}),
                all_slots,
            ),
            Course(
                "Bases de Datos",
                24,
                frozenset({"computers", "databases"}),
                all_slots,
            ),
            Course(
                "Diseño Gráfico",
                22,
                frozenset({"computers", "design"}),
                frozenset({0, 1, 2, 3}),
            ),
            Course(
                "Redes",
                20,
                frozenset({"computers", "networking"}),
                all_slots,
            ),
            Course(
                "Inteligencia Artificial",
                26,
                frozenset({"computers", "python"}),
                frozenset({1, 2, 3, 4}),
            ),
            Course(
                "Ofimática",
                35,
                frozenset({"computers", "office"}),
                all_slots,
            ),
            Course(
                "Desarrollo Web",
                30,
                frozenset({"computers", "python"}),
                all_slots,
            ),
            Course(
                "Pruebas de Software",
                18,
                frozenset({"computers"}),
                all_slots,
            ),
        ]

        self.rooms = [
            Room(
                "Laboratorio A",
                32,
                frozenset({"computers", "python", "databases"}),
                frozenset({4}),
            ),
            Room(
                "Laboratorio B",
                25,
                frozenset({"computers", "design", "office"}),
                frozenset({2}),
            ),
            Room(
                "Laboratorio C",
                40,
                frozenset({"computers", "python", "office", "databases"}),
                frozenset(),
            ),
            Room(
                "Laboratorio D",
                30,
                frozenset({"computers", "networking", "python"}),
                frozenset({0}),
            ),
        ]


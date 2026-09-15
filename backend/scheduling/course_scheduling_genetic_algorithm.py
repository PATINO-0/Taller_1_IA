import random

from collections import Counter, defaultdict

from backend.core.evolution_result import EvolutionResult
from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.core.selection import tournament_select
from backend.scheduling.scheduling_dataset import SchedulingDataset


class CourseSchedulingGeneticAlgorithm:
    """Algoritmo genético de horarios."""

    def __init__(
        self,
        dataset: SchedulingDataset,
        config: GeneticAlgorithmConfig,
    ) -> None:
        self.dataset = dataset
        self.config = config
        self.rng = random.Random(config.seed)

    def _create_individual(self) -> list[tuple[int, int]]:
        return [
            (
                self.rng.randrange(len(self.dataset.rooms)),
                self.rng.randrange(len(self.dataset.slots)),
            )
            for _ in self.dataset.courses
        ]

    def _create_population(self) -> list[list[tuple[int, int]]]:
        return [
            self._create_individual()
            for _ in range(self.config.population_size)
        ]

    def evaluate(
        self,
        individual: list[tuple[int, int]],
    ) -> tuple[float, float, float, list[str]]:
        """Calcula las penalizaciones."""

        hard_penalty = 0.0
        soft_penalty = 0.0
        reasons: list[str] = []
        assignments: dict[tuple[int, int], list[int]] = defaultdict(list)
        slot_usage: Counter[int] = Counter()

        for course_index, (room_index, slot_index) in enumerate(individual):
            course = self.dataset.courses[course_index]
            room = self.dataset.rooms[room_index]
            assignments[(room_index, slot_index)].append(course_index)
            slot_usage[slot_index] += 1

            if course.students > room.capacity:
                excess = course.students - room.capacity
                hard_penalty += 100 + excess * 20
                reasons.append(
                    f"{course.name}: sobrecupo de {excess} estudiantes."
                )

            missing_resources = course.required_resources - room.resources

            if missing_resources:
                hard_penalty += 180 * len(missing_resources)
                reasons.append(
                    f"{course.name}: faltan recursos "
                    f"{', '.join(sorted(missing_resources))}."
                )

            if slot_index in room.blocked_slots:
                hard_penalty += 300
                reasons.append(
                    f"{course.name}: sala bloqueada en esta franja."
                )

            if slot_index not in course.allowed_slots:
                hard_penalty += 260
                reasons.append(f"{course.name}: franja no permitida.")

            # Penalización blanda: evitar desperdicio excesivo.
            if room.capacity >= course.students:
                soft_penalty += (room.capacity - course.students) * 0.25

        for (room_index, slot_index), course_indexes in assignments.items():
            if len(course_indexes) > 1:
                collisions = len(course_indexes) - 1
                hard_penalty += collisions * 500
                reasons.append(
                    "Colisión: "
                    f"{len(course_indexes)} cursos usan "
                    f"{self.dataset.rooms[room_index].name} en "
                    f"{self.dataset.slots[slot_index]}."
                )

        counts = [
            slot_usage[index]
            for index in range(len(self.dataset.slots))
        ]

        if counts:
            soft_penalty += (max(counts) - min(counts)) * 4

        total_penalty = hard_penalty + soft_penalty
        return total_penalty, hard_penalty, soft_penalty, reasons

    def _score(self, individual: list[tuple[int, int]]) -> float:
        return self.evaluate(individual)[0]

    def _crossover(
        self,
        parent_a: list[tuple[int, int]],
        parent_b: list[tuple[int, int]],
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        child_a: list[tuple[int, int]] = []
        child_b: list[tuple[int, int]] = []

        for gene_a, gene_b in zip(parent_a, parent_b, strict=True):
            if self.rng.random() < 0.5:
                child_a.append(gene_a)
                child_b.append(gene_b)
            else:
                child_a.append(gene_b)
                child_b.append(gene_a)

        return child_a, child_b

    def _mutate(
        self,
        individual: list[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        mutated = individual.copy()
        gene_index = self.rng.randrange(len(mutated))
        room_index, slot_index = mutated[gene_index]

        if self.rng.random() < 0.5:
            room_index = self.rng.randrange(len(self.dataset.rooms))
        else:
            slot_index = self.rng.randrange(len(self.dataset.slots))

        mutated[gene_index] = room_index, slot_index
        return mutated

    def run(self) -> EvolutionResult:
        population = self._create_population()
        history: list[dict[str, float]] = []
        global_best: list[tuple[int, int]] | None = None
        global_best_total = float("inf")
        global_best_hard = float("inf")
        best_generation = 0
        valid_stagnation = 0

        for generation in range(self.config.max_generations + 1):
            population.sort(key=self._score)
            best = population[0]
            total, hard, soft, _ = self.evaluate(best)
            average = sum(self._score(item) for item in population) / len(
                population
            )

            if total + 1e-9 < global_best_total:
                global_best = best.copy()
                global_best_total = total
                global_best_hard = hard
                best_generation = generation
                valid_stagnation = 0
            elif global_best_hard == 0:
                valid_stagnation += 1

            history.append(
                {
                    "generation": float(generation),
                    "best": round(global_best_total, 3),
                    "average": round(average, 3),
                    "hard_penalty": round(global_best_hard, 3),
                }
            )

            if global_best_hard == 0 and valid_stagnation >= 100:
                break

            elite_count = min(
                self.config.elitism_count,
                len(population),
            )
            next_population = [
                item.copy()
                for item in population[:elite_count]
            ]

            while len(next_population) < self.config.population_size:
                parent_a = tournament_select(
                    population,
                    self._score,
                    self.rng,
                    self.config.tournament_size,
                    maximize=False,
                )
                parent_b = tournament_select(
                    population,
                    self._score,
                    self.rng,
                    self.config.tournament_size,
                    maximize=False,
                )
                child_a, child_b = self._crossover(parent_a, parent_b)

                if self.rng.random() < self.config.mutation_rate:
                    child_a = self._mutate(child_a)

                if self.rng.random() < self.config.mutation_rate:
                    child_b = self._mutate(child_b)

                next_population.append(child_a)

                if len(next_population) < self.config.population_size:
                    next_population.append(child_b)

            population = next_population

        assert global_best is not None

        total, hard, soft, reasons = self.evaluate(global_best)
        serialized = [
            [room_index, slot_index]
            for room_index, slot_index in global_best
        ]
        return EvolutionResult(
            best_individual=serialized,
            best_score=round(total, 3),
            generation=best_generation,
            solved=hard == 0,
            history=history,
            metadata={
                "hard_penalty": round(hard, 3),
                "soft_penalty": round(soft, 3),
                "reasons": reasons,
                "executed_generations": len(history) - 1,
            },
        )


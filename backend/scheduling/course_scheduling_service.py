from statistics import mean

from backend.core.genetic_algorithm_config import GeneticAlgorithmConfig
from backend.scheduling.course_scheduling_genetic_algorithm import (
    CourseSchedulingGeneticAlgorithm,
)
from backend.scheduling.scheduling_dataset import SchedulingDataset
from backend.schemas.scheduling_experiment_request import (
    SchedulingExperimentRequest,
)
from backend.schemas.scheduling_request import SchedulingRequest


class CourseSchedulingService:
    """Gestiona el problema de horarios."""

    def _serialize_dataset(self, dataset: SchedulingDataset) -> dict:
        return {
            "courses": [
                {
                    "name": course.name,
                    "students": course.students,
                    "required_resources": sorted(course.required_resources),
                    "allowed_slots": [
                        dataset.slots[index]
                        for index in sorted(course.allowed_slots)
                    ],
                }
                for course in dataset.courses
            ],
            "rooms": [
                {
                    "name": room.name,
                    "capacity": room.capacity,
                    "resources": sorted(room.resources),
                    "blocked_slots": [
                        dataset.slots[index]
                        for index in sorted(room.blocked_slots)
                    ],
                }
                for room in dataset.rooms
            ],
            "slots": dataset.slots,
        }

    def run(self, request: SchedulingRequest) -> dict:
        dataset = SchedulingDataset()
        elitism_count = (
            min(request.elitism_count, request.population_size)
            if request.use_elitism
            else 0
        )
        config = GeneticAlgorithmConfig(
            population_size=request.population_size,
            mutation_rate=request.mutation_rate,
            max_generations=request.max_generations,
            elitism_count=elitism_count,
            seed=request.seed,
        )
        result = CourseSchedulingGeneticAlgorithm(
            dataset,
            config,
        ).run().to_dict()
        schedule = []

        for course_index, gene in enumerate(result["best_individual"]):
            room_index, slot_index = gene
            course = dataset.courses[course_index]
            room = dataset.rooms[room_index]
            schedule.append(
                {
                    "course": course.name,
                    "students": course.students,
                    "room": room.name,
                    "room_capacity": room.capacity,
                    "slot": dataset.slots[slot_index],
                }
            )

        schedule.sort(key=lambda row: (row["slot"], row["room"]))
        result["schedule"] = schedule
        result["dataset"] = self._serialize_dataset(dataset)
        result["parameters"] = request.model_dump()
        return result

    def experiment(self, request: SchedulingExperimentRequest) -> dict:
        dataset = SchedulingDataset()
        rows: list[dict] = []

        for use_elitism in [False, True]:
            run_results: list[dict] = []

            for run_index in range(request.runs):
                config = GeneticAlgorithmConfig(
                    population_size=request.population_size,
                    mutation_rate=request.mutation_rate,
                    max_generations=request.max_generations,
                    elitism_count=3 if use_elitism else 0,
                    seed=30_000 + run_index,
                )
                result = CourseSchedulingGeneticAlgorithm(
                    dataset,
                    config,
                ).run()
                run_results.append(
                    {
                        "total_penalty": result.best_score,
                        "hard_penalty": result.metadata["hard_penalty"],
                        "generation": result.generation,
                        "valid": result.solved,
                    }
                )

            rows.append(
                {
                    "elitism": use_elitism,
                    "runs": request.runs,
                    "valid_rate": (
                        sum(1 for run in run_results if run["valid"])
                        / request.runs
                    ),
                    "best_total_penalty": min(
                        run["total_penalty"] for run in run_results
                    ),
                    "average_total_penalty": round(
                        mean(run["total_penalty"] for run in run_results), 3
                    ),
                    "average_hard_penalty": round(
                        mean(run["hard_penalty"] for run in run_results), 3
                    ),
                    "average_best_generation": round(
                        mean(run["generation"] for run in run_results), 2
                    ),
                }
            )

        return {
            "rows": rows,
            "dataset": self._serialize_dataset(dataset),
        }


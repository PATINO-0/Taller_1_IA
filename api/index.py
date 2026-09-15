from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.knapsack.knapsack_service import KnapsackService
from backend.n_queens.n_queens_service import NQueensService
from backend.scheduling.course_scheduling_service import CourseSchedulingService
from backend.schemas.knapsack_experiment_request import (
    KnapsackExperimentRequest,
)
from backend.schemas.knapsack_request import KnapsackRequest
from backend.schemas.n_queens_experiment_request import (
    NQueensExperimentRequest,
)
from backend.schemas.n_queens_request import NQueensRequest
from backend.schemas.scheduling_experiment_request import (
    SchedulingExperimentRequest,
)
from backend.schemas.scheduling_request import SchedulingRequest
from backend.schemas.tsp_experiment_request import TSPExperimentRequest
from backend.schemas.tsp_request import TSPRequest
from backend.tsp.tsp_service import TSPService

app = FastAPI(
    title="Taller 1 - Inteligencia Artificial",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    description=(
        "API de algoritmos genéticos para N-Reinas, "
        "TSP, horarios y mochila."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

n_queens_service = NQueensService()
tsp_service = TSPService()
scheduling_service = CourseSchedulingService()
knapsack_service = KnapsackService()


@app.get("/api")
def api_root() -> dict[str, str]:
    return {
        "message": "Taller 1 IA API",
        "status": "ok",
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/n-queens/run")
def run_n_queens(request: NQueensRequest) -> dict:
    return n_queens_service.run(request)


@app.post("/api/n-queens/experiment")
def experiment_n_queens(
    request: NQueensExperimentRequest,
) -> dict:
    return n_queens_service.experiment(request)


@app.post("/api/tsp/run")
def run_tsp(request: TSPRequest) -> dict:
    return tsp_service.run(request)


@app.post("/api/tsp/experiment")
def experiment_tsp(
    request: TSPExperimentRequest,
) -> dict:
    return tsp_service.experiment(request)


@app.post("/api/scheduling/run")
def run_scheduling(
    request: SchedulingRequest,
) -> dict:
    return scheduling_service.run(request)


@app.post("/api/scheduling/experiment")
def experiment_scheduling(
    request: SchedulingExperimentRequest,
) -> dict:
    return scheduling_service.experiment(request)


@app.post("/api/knapsack/run")
def run_knapsack(request: KnapsackRequest) -> dict:
    return knapsack_service.run(request)


@app.post("/api/knapsack/experiment")
def experiment_knapsack(
    request: KnapsackExperimentRequest,
) -> dict:
    try:
        return knapsack_service.experiment(request)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

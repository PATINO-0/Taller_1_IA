from fastapi.testclient import TestClient

from api.index import app


client = TestClient(app)


def test_vercel_gateway_runs_n_queens() -> None:
    response = client.post(
        "/api?endpoint=n-queens/run",
        json={
            "n": 8,
            "population_size": 100,
            "mutation_rate": 0.1,
            "max_generations": 1000,
            "elitism_count": 2,
            "seed": 7,
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["solved"]
    assert result["history"]
    assert result["best_score"] == 0


def test_vercel_gateway_rejects_unknown_operation() -> None:
    response = client.post(
        "/api?endpoint=unknown",
        json={},
    )

    assert response.status_code == 404

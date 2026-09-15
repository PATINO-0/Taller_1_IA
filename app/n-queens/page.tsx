"use client";

import {
  useState,
} from "react";

import {
  ErrorMessage,
} from "@/components/ErrorMessage";

import {
  LineChart,
} from "@/components/LineChart";

import {
  MetricCard,
} from "@/components/MetricCard";

import {
  postJson,
} from "@/lib/api";

import type {
  BaseResult,
} from "@/lib/types";


type NQueensResult =
  BaseResult & {
    best_individual: number[];
    conflicts: number;
  };


type ExperimentRow = {
  n: number;
  population_size: number;
  mutation_rate: number;
  runs: number;
  success_rate: number;
  best_generation: number | null;
  worst_generation: number | null;
  average_generation: number | null;
  average_final_conflicts: number;
};


export default function NQueensPage() {
  const [
    n,
    setN,
  ] = useState(8);

  const [
    populationSize,
    setPopulationSize,
  ] = useState(100);

  const [
    mutationRate,
    setMutationRate,
  ] = useState(0.1);

  const [
    maxGenerations,
    setMaxGenerations,
  ] = useState(1000);

  const [
    result,
    setResult,
  ] = useState<NQueensResult | null>(
    null,
  );

  const [
    experiment,
    setExperiment,
  ] = useState<ExperimentRow[]>(
    [],
  );

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    experimentLoading,
    setExperimentLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(
    null,
  );


  async function runAlgorithm() {
    setLoading(true);
    setError(null);

    try {
      const data =
        await postJson<NQueensResult>(
          "/api/n-queens/run",
          {
            n,
            population_size:
              populationSize,
            mutation_rate:
              mutationRate,
            max_generations:
              maxGenerations,
            elitism_count: 2,
          },
        );

      setResult(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Error inesperado",
      );
    } finally {
      setLoading(false);
    }
  }


  async function runExperiment() {
    setExperimentLoading(true);
    setError(null);

    try {
      const data = await postJson<{
        rows: ExperimentRow[];
      }>(
        "/api/n-queens/experiment",
        {
          runs: 10,
          n_values: [
            6,
            8,
          ],
          population_sizes: [
            30,
            60,
            120,
          ],
          mutation_rates: [
            0.05,
            0.1,
            0.2,
          ],
          max_generations: 1000,
        },
      );

      setExperiment(
        data.rows,
      );
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Error inesperado",
      );
    } finally {
      setExperimentLoading(false);
    }
  }


  return (
    <div className="problem-page queens">
      <section className="problem-hero">
        <span className="eyebrow">
          Problema base · Permutaciones
        </span>

        <h1>
          N-Reinas
        </h1>

        <p>
          Cada índice representa una columna
          y cada valor la fila de la reina.
          La función objetivo minimiza los
          conflictos hasta llegar a cero.
        </p>
      </section>

      <div className="workspace">
        <aside className="panel controls">
          <h2>
            Parámetros
          </h2>

          <div className="field">
            <label>
              N
            </label>

            <select
              value={n}
              onChange={(event) =>
                setN(
                  Number(
                    event.target.value,
                  ),
                )
              }
            >
              <option value={6}>
                6 reinas
              </option>

              <option value={8}>
                8 reinas
              </option>
            </select>
          </div>

          <div className="field">
            <label>
              Tamaño de población
            </label>

            <input
              type="number"
              min={10}
              value={populationSize}
              onChange={(event) =>
                setPopulationSize(
                  Number(
                    event.target.value,
                  ),
                )
              }
            />
          </div>

          <div className="field">
            <label>
              Tasa de mutación
            </label>

            <select
              value={mutationRate}
              onChange={(event) =>
                setMutationRate(
                  Number(
                    event.target.value,
                  ),
                )
              }
            >
              <option value={0.05}>
                0.05
              </option>

              <option value={0.1}>
                0.10
              </option>

              <option value={0.2}>
                0.20
              </option>
            </select>
          </div>

          <div className="field">
            <label>
              Máximo de generaciones
            </label>

            <input
              type="number"
              min={1}
              value={maxGenerations}
              onChange={(event) =>
                setMaxGenerations(
                  Number(
                    event.target.value,
                  ),
                )
              }
            />
          </div>

          <div className="actions">
            <button
              className="button"
              disabled={loading}
              onClick={runAlgorithm}
            >
              {loading
                ? "Ejecutando..."
                : "Resolver N-Reinas"}
            </button>

            <button
              className="button secondary"
              disabled={
                experimentLoading
              }
              onClick={
                runExperiment
              }
            >
              {experimentLoading
                ? "Experimentando..."
                : "Ejecutar matriz de pruebas"}
            </button>
          </div>

          <ErrorMessage
            message={error}
          />
        </aside>

        <section className="result-stack">
          {!result ? (
            <div className="panel empty-state">
              Configura los parámetros y
              ejecuta el algoritmo.
            </div>
          ) : (
            <>
              <div className="metrics">
                <MetricCard
                  label="Conflictos"
                  value={
                    result.conflicts
                  }
                  help="Objetivo: 0"
                />

                <MetricCard
                  label="Mejor generación"
                  value={
                    result.generation
                  }
                />

                <MetricCard
                  label="Estado"
                  value={
                    result.solved
                      ? "Óptimo"
                      : "No óptimo"
                  }
                />
              </div>

              <section className="panel">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">
                      Solución
                    </span>

                    <h2>
                      Tablero {n} × {n}
                    </h2>
                  </div>

                  <span
                    className={
                      result.solved
                        ? "status-good"
                        : "status-bad"
                    }
                  >
                    {result.solved
                      ? "Sin conflictos"
                      : `${result.conflicts} conflictos`}
                  </span>
                </div>

                <div
                  className="queen-board"
                  style={{
                    gridTemplateColumns:
                      `repeat(${n}, 1fr)`,
                  }}
                >
                  {Array.from({
                    length:
                      n * n,
                  }).map(
                    (_, index) => {
                      const row =
                        Math.floor(
                          index / n,
                        );

                      const column =
                        index % n;

                      const hasQueen =
                        result
                          .best_individual[
                          column
                        ] === row;

                      return (
                        <div
                          className={
                            (
                              row
                              + column
                            ) % 2 === 0
                              ? "queen-cell light"
                              : "queen-cell dark"
                          }
                          key={index}
                        >
                          {hasQueen
                            ? "♛"
                            : ""}
                        </div>
                      );
                    },
                  )}
                </div>

                <p className="muted">
                  Cromosoma:{" "}
                  {result
                    .best_individual
                    .join(" · ")}
                </p>
              </section>

              <LineChart
                data={
                  result.history
                }
                title="Conflictos por generación"
              />
            </>
          )}

          {experiment.length > 0 ? (
            <section className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    10 corridas por configuración
                  </span>

                  <h2>
                    Experimento N=6 y N=8
                  </h2>
                </div>
              </div>

              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>N</th>
                      <th>Población</th>
                      <th>Mutación</th>
                      <th>Éxito</th>
                      <th>Mejor gen.</th>
                      <th>Promedio gen.</th>
                      <th>Conflictos</th>
                    </tr>
                  </thead>

                  <tbody>
                    {experiment.map(
                      (row) => (
                        <tr
                          key={`${row.n}-${row.population_size}-${row.mutation_rate}`}
                        >
                          <td>
                            {row.n}
                          </td>

                          <td>
                            {
                              row.population_size
                            }
                          </td>

                          <td>
                            {
                              row.mutation_rate
                            }
                          </td>

                          <td>
                            {(
                              row.success_rate
                              * 100
                            ).toFixed(0)}
                            %
                          </td>

                          <td>
                            {
                              row.best_generation
                              ?? "—"
                            }
                          </td>

                          <td>
                            {
                              row
                                .average_generation
                                ?.toFixed(1)
                              ?? "—"
                            }
                          </td>

                          <td>
                            {
                              row
                                .average_final_conflicts
                                .toFixed(2)
                            }
                          </td>
                        </tr>
                      ),
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          ) : null}
        </section>
      </div>
    </div>
  );
}


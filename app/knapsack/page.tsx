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


type Item = {
  name: string;
  weight: number;
  value: number;
};


type KnapsackResult =
  BaseResult & {
    best_individual: number[];
    weight: number;
    value: number;
    selected_items: string[];
    items: Item[];

    exact_reference: {
      value: number;
      weight: number;
      chromosome: number[];
    };

    optimality_gap: number;
  };


type ExperimentRow = {
  capacity: number;
  strategy: string;
  runs: number;
  valid_rate: number;
  best_value: number;
  worst_value: number;
  average_value: number;
  average_weight:
    number | null;
  average_best_generation: number;
  exact_optimum: number;
  average_gap: number;
};


export default function KnapsackPage() {
  const [
    capacity,
    setCapacity,
  ] = useState(35);

  const [
    populationSize,
    setPopulationSize,
  ] = useState(120);

  const [
    mutationRate,
    setMutationRate,
  ] = useState(0.03);

  const [
    constraintStrategy,
    setConstraintStrategy,
  ] = useState(
    "repair",
  );

  const [
    maxGenerations,
    setMaxGenerations,
  ] = useState(600);

  const [
    result,
    setResult,
  ] = useState<
    KnapsackResult | null
  >(null);

  const [
    experiment,
    setExperiment,
  ] = useState<
    ExperimentRow[]
  >([]);

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
  ] = useState<
    string | null
  >(null);


  async function runAlgorithm() {
    setLoading(true);
    setError(null);

    try {
      const data =
        await postJson<KnapsackResult>(
          "/api/knapsack/run",
          {
            capacity,
            population_size:
              populationSize,
            mutation_rate:
              mutationRate,
            constraint_strategy:
              constraintStrategy,
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


  async function compareStrategies() {
    setExperimentLoading(true);
    setError(null);

    try {
      const data = await postJson<{
        rows: ExperimentRow[];
      }>(
        "/api/knapsack/experiment",
        {
          capacities: [
            35,
            50,
          ],
          strategies: [
            "penalty",
            "repair",
          ],
          runs: 10,
          population_size:
            populationSize,
          mutation_rate:
            mutationRate,
          max_generations:
            maxGenerations,
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
    <div className="problem-page knapsack">
      <section className="problem-hero">
        <span className="eyebrow">
          Problema 04 · Cromosoma binario
        </span>

        <h1>
          Problema de la Mochila
        </h1>

        <p>
          Cada gen indica si un objeto se
          selecciona o no. El objetivo consiste
          en maximizar el valor total sin superar
          la capacidad disponible.
        </p>
      </section>

      <div className="workspace">
        <aside className="panel controls">
          <h2>
            Parámetros
          </h2>

          <div className="field">
            <label>
              Capacidad
            </label>

            <select
              value={capacity}
              onChange={(event) =>
                setCapacity(
                  Number(
                    event.target.value,
                  ),
                )
              }
            >
              <option value={35}>
                35 unidades
              </option>

              <option value={50}>
                50 unidades
              </option>
            </select>
          </div>

          <div className="field">
            <label>
              Población
            </label>

            <input
              type="number"
              min={20}
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
              Tasa de mutación por bit
            </label>

            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={mutationRate}
              onChange={(event) =>
                setMutationRate(
                  Number(
                    event.target.value,
                  ),
                )
              }
            />
          </div>

          <div className="field">
            <label>
              Manejo de restricciones
            </label>

            <select
              value={
                constraintStrategy
              }
              onChange={(event) =>
                setConstraintStrategy(
                  event.target.value,
                )
              }
            >
              <option value="repair">
                Reparación
              </option>

              <option value="penalty">
                Penalización
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
              onClick={
                runAlgorithm
              }
            >
              {loading
                ? "Optimizando..."
                : "Llenar mochila"}
            </button>

            <button
              className="button secondary"
              disabled={
                experimentLoading
              }
              onClick={
                compareStrategies
              }
            >
              {experimentLoading
                ? "Comparando..."
                : "Comparar estrategias"}
            </button>
          </div>

          <ErrorMessage
            message={error}
          />
        </aside>

        <section className="result-stack">
          {!result ? (
            <div className="panel empty-state">
              Ejecuta el algoritmo para
              seleccionar objetos.
            </div>
          ) : (
            <>
              <div className="metrics">
                <MetricCard
                  label="Valor total"
                  value={
                    result.value
                  }
                  help="Mayor es mejor"
                />

                <MetricCard
                  label="Peso"
                  value={`${result.weight} / ${capacity}`}
                />

                <MetricCard
                  label="Brecha al óptimo"
                  value={
                    result.optimality_gap
                  }
                  help="Referencia exacta"
                />
              </div>

              <section className="panel">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">
                      Cromosoma
                    </span>

                    <h2>
                      Contenido de la mochila
                    </h2>
                  </div>

                  <span
                    className={
                      result.weight <= capacity
                        ? "status-good"
                        : "status-bad"
                    }
                  >
                    {
                      result.weight
                      <= capacity
                        ? "Factible"
                        : "Sobrecupo"
                    }
                  </span>
                </div>

                <div className="item-grid">
                  {result.items.map(
                    (item, index) => {
                      const selected =
                        result
                          .best_individual[
                          index
                        ] === 1;

                      return (
                        <article
                          className={
                            selected
                              ? "item-card selected"
                              : "item-card"
                          }
                          key={item.name}
                        >
                          <span className="binary-bit">
                            {selected
                              ? 1
                              : 0}
                          </span>

                          <b>
                            {item.name}
                          </b>

                          <small>
                            Peso{" "}
                            {item.weight}
                            {" · "}
                            Valor{" "}
                            {item.value}
                          </small>
                        </article>
                      );
                    },
                  )}
                </div>

                <p className="muted">
                  Óptimo exacto de referencia:
                  valor{" "}
                  {
                    result
                      .exact_reference
                      .value
                  }
                  , peso{" "}
                  {
                    result
                      .exact_reference
                      .weight
                  }
                  .
                </p>
              </section>

              <LineChart
                data={
                  result.history
                }
                title="Aptitud por generación"
              />
            </>
          )}

          {experiment.length > 0 ? (
            <section className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    10 corridas por caso
                  </span>

                  <h2>
                    Penalización vs. reparación
                  </h2>
                </div>
              </div>

              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>
                        Capacidad
                      </th>
                      <th>
                        Estrategia
                      </th>
                      <th>
                        Factibles
                      </th>
                      <th>
                        Mejor valor
                      </th>
                      <th>
                        Peor
                      </th>
                      <th>
                        Promedio
                      </th>
                      <th>
                        Óptimo
                      </th>
                      <th>
                        Brecha
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {experiment.map(
                      (row) => (
                        <tr
                          key={`${row.capacity}-${row.strategy}`}
                        >
                          <td>
                            {
                              row.capacity
                            }
                          </td>

                          <td>
                            {
                              row.strategy
                            }
                          </td>

                          <td>
                            {(
                              row.valid_rate
                              * 100
                            ).toFixed(0)}
                            %
                          </td>

                          <td>
                            {
                              row.best_value
                            }
                          </td>

                          <td>
                            {
                              row.worst_value
                            }
                          </td>

                          <td>
                            {
                              row.average_value
                                .toFixed(1)
                            }
                          </td>

                          <td>
                            {
                              row.exact_optimum
                            }
                          </td>

                          <td>
                            {
                              row.average_gap
                                .toFixed(1)
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


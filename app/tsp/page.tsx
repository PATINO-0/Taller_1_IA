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
  RouteMap,
} from "@/components/RouteMap";

import {
  postJson,
} from "@/lib/api";

import type {
  BaseResult,
} from "@/lib/types";


type TSPResult =
  BaseResult & {
    best_individual: number[];
    route: number[];
    distance: number;
    coordinates: number[][];
  };


type ExperimentRow = {
  mutation_strategy: string;
  mutation_rate: number;
  runs: number;
  best_distance: number;
  worst_distance: number;
  average_distance: number;
  average_best_generation: number;
  best_route: number[];
};


export default function TSPPage() {
  const [
    cityCount,
    setCityCount,
  ] = useState(10);

  const [
    populationSize,
    setPopulationSize,
  ] = useState(150);

  const [
    mutationRate,
    setMutationRate,
  ] = useState(0.1);

  const [
    mutationStrategy,
    setMutationStrategy,
  ] = useState(
    "inversion",
  );

  const [
    maxGenerations,
    setMaxGenerations,
  ] = useState(1200);

  const [
    result,
    setResult,
  ] = useState<TSPResult | null>(
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
        await postJson<TSPResult>(
          "/api/tsp/run",
          {
            city_count:
              cityCount,
            population_size:
              populationSize,
            mutation_rate:
              mutationRate,
            mutation_strategy:
              mutationStrategy,
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
        "/api/tsp/experiment",
        {
          city_count:
            cityCount,
          population_size:
            populationSize,
          mutation_rates: [
            0.05,
            0.2,
          ],
          mutation_strategies: [
            "swap",
            "inversion",
          ],
          runs: 10,
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
    <div className="problem-page tsp">
      <section className="problem-hero">
        <span className="eyebrow">
          Problema 02 · Ruta mínima
        </span>

        <h1>
          Agente Viajero — TSP
        </h1>

        <p>
          La ruta es una permutación de ciudades.
          Se utiliza OX para conservar rutas
          válidas y se compara mutación swap
          frente a inversión.
        </p>
      </section>

      <div className="workspace">
        <aside className="panel controls">
          <h2>
            Parámetros
          </h2>

          <div className="field">
            <label>
              Número de ciudades
            </label>

            <select
              value={cityCount}
              onChange={(event) =>
                setCityCount(
                  Number(
                    event.target.value,
                  ),
                )
              }
            >
              <option value={8}>
                8 ciudades
              </option>

              <option value={10}>
                10 ciudades
              </option>

              <option value={15}>
                15 ciudades
              </option>
            </select>
          </div>

          <div className="field">
            <label>
              Tamaño de población
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
              Tasa de mutación
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
              Estrategia de mutación
            </label>

            <select
              value={
                mutationStrategy
              }
              onChange={(event) =>
                setMutationStrategy(
                  event.target.value,
                )
              }
            >
              <option value="inversion">
                Inversión
              </option>

              <option value="swap">
                Intercambio (swap)
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
                ? "Buscando ruta..."
                : "Optimizar ruta"}
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
                ? "Comparando..."
                : "Comparar mutaciones"}
            </button>
          </div>

          <ErrorMessage
            message={error}
          />
        </aside>

        <section className="result-stack">
          {!result ? (
            <div className="panel empty-state">
              Ejecuta el TSP para visualizar
              la mejor ruta encontrada.
            </div>
          ) : (
            <>
              <div className="metrics">
                <MetricCard
                  label="Distancia"
                  value={
                    result.distance
                      .toFixed(3)
                  }
                  help="Menor es mejor"
                />

                <MetricCard
                  label="Mejor generación"
                  value={
                    result.generation
                  }
                />

                <MetricCard
                  label="Ciudades"
                  value={cityCount}
                />
              </div>

              <section className="panel">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">
                      Ruta encontrada
                    </span>

                    <h2>
                      Mapa cartesiano
                    </h2>
                  </div>
                </div>

                <RouteMap
                  route={
                    result.route
                  }
                  coordinates={
                    result.coordinates
                  }
                />

                <div>
                  {result.route.map(
                    (city, index) => (
                      <span
                        className="code-chip"
                        key={`${city}-${index}`}
                      >
                        {city}
                      </span>
                    ),
                  )}
                </div>
              </section>

              <LineChart
                data={
                  result.history
                }
                title="Distancia por generación"
              />
            </>
          )}

          {experiment.length > 0 ? (
            <section className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    10 corridas por combinación
                  </span>

                  <h2>
                    Swap vs. inversión
                  </h2>
                </div>
              </div>

              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>
                        Mutación
                      </th>
                      <th>
                        Tasa
                      </th>
                      <th>
                        Mejor
                      </th>
                      <th>
                        Peor
                      </th>
                      <th>
                        Promedio
                      </th>
                      <th>
                        Gen. promedio
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {experiment.map(
                      (row) => (
                        <tr
                          key={`${row.mutation_strategy}-${row.mutation_rate}`}
                        >
                          <td>
                            {
                              row.mutation_strategy
                            }
                          </td>

                          <td>
                            {
                              row.mutation_rate
                            }
                          </td>

                          <td>
                            {
                              row.best_distance
                                .toFixed(3)
                            }
                          </td>

                          <td>
                            {
                              row.worst_distance
                                .toFixed(3)
                            }
                          </td>

                          <td>
                            {
                              row.average_distance
                                .toFixed(3)
                            }
                          </td>

                          <td>
                            {
                              row.average_best_generation
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


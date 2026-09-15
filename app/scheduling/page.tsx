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


type ScheduleRow = {
  course: string;
  students: number;
  room: string;
  room_capacity: number;
  slot: string;
};


type Dataset = {
  courses: {
    name: string;
    students: number;
    required_resources: string[];
    allowed_slots: string[];
  }[];

  rooms: {
    name: string;
    capacity: number;
    resources: string[];
    blocked_slots: string[];
  }[];

  slots: string[];
};


type SchedulingResult =
  BaseResult & {
    schedule: ScheduleRow[];
    dataset: Dataset;

    metadata: {
      hard_penalty: number;
      soft_penalty: number;
      reasons: string[];
      executed_generations: number;
    };
  };


type ExperimentRow = {
  elitism: boolean;
  runs: number;
  valid_rate: number;
  best_total_penalty: number;
  average_total_penalty: number;
  average_hard_penalty: number;
  average_best_generation: number;
};


export default function SchedulingPage() {
  const [
    populationSize,
    setPopulationSize,
  ] = useState(180);

  const [
    mutationRate,
    setMutationRate,
  ] = useState(0.12);

  const [
    maxGenerations,
    setMaxGenerations,
  ] = useState(1500);

  const [
    useElitism,
    setUseElitism,
  ] = useState(true);

  const [
    result,
    setResult,
  ] = useState<
    SchedulingResult | null
  >(null);

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
        await postJson<SchedulingResult>(
          "/api/scheduling/run",
          {
            population_size:
              populationSize,
            mutation_rate:
              mutationRate,
            max_generations:
              maxGenerations,
            use_elitism:
              useElitism,
            elitism_count: 3,
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


  async function compareElitism() {
    setExperimentLoading(true);
    setError(null);

    try {
      const data = await postJson<{
        rows: ExperimentRow[];
      }>(
        "/api/scheduling/experiment",
        {
          population_size:
            populationSize,
          mutation_rate:
            mutationRate,
          max_generations:
            maxGenerations,
          runs: 10,
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
    <div className="problem-page scheduling">
      <section className="problem-hero">
        <span className="eyebrow">
          Problema 03 · Restricciones
        </span>

        <h1>
          Asignación de cursos
        </h1>

        <p>
          Ocho cursos deben asignarse entre cuatro
          salas y cinco franjas. Las restricciones
          duras determinan la validez del horario
          y las blandas permiten mejorar la
          distribución.
        </p>
      </section>

      <div className="workspace">
        <aside className="panel controls">
          <h2>
            Parámetros
          </h2>

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

          <div className="field">
            <label>
              Elitismo
            </label>

            <select
              value={
                useElitism
                  ? "yes"
                  : "no"
              }
              onChange={(event) =>
                setUseElitism(
                  event.target.value
                    === "yes",
                )
              }
            >
              <option value="yes">
                Activado
              </option>

              <option value="no">
                Desactivado
              </option>
            </select>
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
                ? "Generando horario..."
                : "Optimizar horario"}
            </button>

            <button
              className="button secondary"
              disabled={
                experimentLoading
              }
              onClick={
                compareElitism
              }
            >
              {experimentLoading
                ? "Comparando..."
                : "Comparar elitismo"}
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
              construir un horario.
            </div>
          ) : (
            <>
              <div className="metrics">
                <MetricCard
                  label="Penalización dura"
                  value={
                    result
                      .metadata
                      .hard_penalty
                      .toFixed(2)
                  }
                  help="Debe llegar a 0"
                />

                <MetricCard
                  label="Penalización blanda"
                  value={
                    result
                      .metadata
                      .soft_penalty
                      .toFixed(2)
                  }
                />

                <MetricCard
                  label="Estado"
                  value={
                    result.solved
                      ? "Válido"
                      : "Con conflictos"
                  }
                />
              </div>

              <section className="panel">
                <div className="section-heading">
                  <div>
                    <span className="eyebrow">
                      Programación final
                    </span>

                    <h2>
                      Horario generado
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
                      ? "Restricciones duras satisfechas"
                      : "Requiere ajustes"}
                  </span>
                </div>

                <div className="table-wrap">
                  <table>
                    <thead>
                      <tr>
                        <th>
                          Franja
                        </th>
                        <th>
                          Curso
                        </th>
                        <th>
                          Estudiantes
                        </th>
                        <th>
                          Sala
                        </th>
                        <th>
                          Capacidad
                        </th>
                      </tr>
                    </thead>

                    <tbody>
                      {result.schedule.map(
                        (row) => (
                          <tr
                            key={
                              row.course
                            }
                          >
                            <td>
                              {row.slot}
                            </td>

                            <td>
                              {row.course}
                            </td>

                            <td>
                              {row.students}
                            </td>

                            <td>
                              {row.room}
                            </td>

                            <td>
                              {
                                row.room_capacity
                              }
                            </td>
                          </tr>
                        ),
                      )}
                    </tbody>
                  </table>
                </div>
              </section>

              <section className="card-grid">
                <article className="panel">
                  <h2>
                    Cursos y requisitos
                  </h2>

                  {result.dataset.courses.map(
                    (course) => (
                      <div
                        className="dataset-row"
                        key={
                          course.name
                        }
                      >
                        <b>
                          {
                            course.name
                          }
                        </b>

                        <span>
                          {
                            course.students
                          }{" "}
                          estudiantes
                        </span>

                        <small>
                          {
                            course
                              .required_resources
                              .join(", ")
                          }
                        </small>
                      </div>
                    ),
                  )}
                </article>

                <article className="panel">
                  <h2>
                    Salas disponibles
                  </h2>

                  {result.dataset.rooms.map(
                    (room) => (
                      <div
                        className="dataset-row"
                        key={
                          room.name
                        }
                      >
                        <b>
                          {room.name}
                        </b>

                        <span>
                          Capacidad{" "}
                          {
                            room.capacity
                          }
                        </span>

                        <small>
                          {
                            room.resources
                              .join(", ")
                          }
                        </small>
                      </div>
                    ),
                  )}
                </article>
              </section>

              <LineChart
                data={
                  result.history
                }
                title="Penalización por generación"
              />
            </>
          )}

          {experiment.length > 0 ? (
            <section className="panel">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">
                    10 corridas
                  </span>

                  <h2>
                    Con y sin elitismo
                  </h2>
                </div>
              </div>

              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>
                        Elitismo
                      </th>
                      <th>
                        Soluciones válidas
                      </th>
                      <th>
                        Mejor penalización
                      </th>
                      <th>
                        Promedio total
                      </th>
                      <th>
                        Penalización dura
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
                          key={String(
                            row.elitism,
                          )}
                        >
                          <td>
                            {row.elitism
                              ? "Sí"
                              : "No"}
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
                              row
                                .best_total_penalty
                                .toFixed(2)
                            }
                          </td>

                          <td>
                            {
                              row
                                .average_total_penalty
                                .toFixed(2)
                            }
                          </td>

                          <td>
                            {
                              row
                                .average_hard_penalty
                                .toFixed(2)
                            }
                          </td>

                          <td>
                            {
                              row
                                .average_best_generation
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


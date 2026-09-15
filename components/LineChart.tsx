import type { HistoryPoint } from "@/lib/types";

type LineChartProps = {
  data: HistoryPoint[];
  title: string;
};

export function LineChart({ data, title }: LineChartProps) {
  if (!data.length) {
    return null;
  }

  const step = Math.max(1, Math.ceil(data.length / 140));
  const sampled = data.filter(
    (_, index) => index % step === 0 || index === data.length - 1,
  );
  const width = 900;
  const height = 280;
  const padding = 34;
  const values = sampled.flatMap((point) => [point.best, point.average]);
  const minY = Math.min(...values);
  const maxY = Math.max(...values);
  const rangeY = Math.max(1, maxY - minY);
  const maxX = Math.max(1, sampled[sampled.length - 1].generation);

  const toPoint = (value: number, generation: number) => {
    const x =
      padding + (generation / maxX) * (width - padding * 2);
    const y =
      height -
      padding -
      ((value - minY) / rangeY) * (height - padding * 2);

    return `${x},${y}`;
  };

  const bestPath = sampled
    .map((point) => toPoint(point.best, point.generation))
    .join(" ");
  const averagePath = sampled
    .map((point) => toPoint(point.average, point.generation))
    .join(" ");

  return (
    <section className="panel chart-panel">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Convergencia</span>
          <h2>{title}</h2>
        </div>

        <div className="legend">
          <span>
            <i className="legend-best" />
            Mejor
          </span>
          <span>
            <i className="legend-average" />
            Promedio
          </span>
        </div>
      </div>

      <svg
        className="line-chart"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={title}
      >
        <line
          x1={padding}
          y1={height - padding}
          x2={width - padding}
          y2={height - padding}
          className="axis"
        />

        <line
          x1={padding}
          y1={padding}
          x2={padding}
          y2={height - padding}
          className="axis"
        />

        <polyline
          points={averagePath}
          fill="none"
          className="average-line"
        />

        <polyline points={bestPath} fill="none" className="best-line" />
      </svg>

      <div className="chart-caption">
        <span>Generación 0</span>
        <span>Generación {data[data.length - 1].generation}</span>
      </div>
    </section>
  );
}


import type { HistoryPoint } from "@/lib/types";

type LineChartProps = {
  data: HistoryPoint[];
  title: string;
};

export function LineChart({ data, title }: LineChartProps) {
  if (!data.length) {
    return null;
  }

  const maximumSamples = 72;
  const sampleCount = Math.min(data.length, maximumSamples);
  const sampled = Array.from({ length: sampleCount }, (_, index) => {
    const sourceIndex =
      sampleCount === 1
        ? 0
        : Math.round((index * (data.length - 1)) / (sampleCount - 1));

    return data[sourceIndex];
  });
  const plotted =
    sampled.length >= 3
      ? sampled
      : Array.from(
          { length: 3 },
          (_, index) => sampled[Math.min(index, sampled.length - 1)],
        );
  const width = 900;
  const height = 520;
  const centerX = width / 2;
  const centerY = height / 2;
  const maximumRadius = 205;
  const values = sampled.flatMap((point) => [point.best, point.average]);
  const minY = Math.min(...values);
  const maxY = Math.max(...values);
  const rangeY = maxY - minY;
  const ringCount = 5;
  const spokeStep = Math.max(1, Math.ceil(plotted.length / 18));
  const labelStep = Math.max(1, Math.ceil(plotted.length / 8));

  const polarPoint = (radius: number, index: number, total: number) => {
    const angle = -Math.PI / 2 + (index / total) * Math.PI * 2;

    return {
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius,
    };
  };

  const valueRadius = (value: number) => {
    const normalized = rangeY === 0 ? 0.5 : (value - minY) / rangeY;
    return maximumRadius * (0.12 + normalized * 0.88);
  };

  const polygonFor = (selector: (point: HistoryPoint) => number) =>
    plotted
      .map((point, index) => {
        const position = polarPoint(
          valueRadius(selector(point)),
          index,
          plotted.length,
        );
        return `${position.x},${position.y}`;
      })
      .join(" ");

  const bestPolygon = polygonFor((point) => point.best);
  const averagePolygon = polygonFor((point) => point.average);
  const formatValue = (value: number) =>
    new Intl.NumberFormat("es-CO", {
      maximumFractionDigits: 2,
    }).format(value);

  return (
    <section className="panel chart-panel">
      <div className="section-heading">
        <div>
          <span className="eyebrow">Convergencia · Vista spider</span>
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
        className="spider-chart"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={title}
      >
        <title>{title}</title>
        <desc>
          Gráfica radial de {sampled.length} muestras uniformes entre las
          generaciones {data[0].generation} y {data[data.length - 1].generation}.
        </desc>

        {Array.from({ length: ringCount }, (_, ringIndex) => {
          const radius = (maximumRadius * (ringIndex + 1)) / ringCount;
          const points = plotted
            .map((_, index) => {
              const position = polarPoint(radius, index, plotted.length);
              return `${position.x},${position.y}`;
            })
            .join(" ");

          return (
            <polygon
              className={
                ringIndex === ringCount - 1
                  ? "spider-grid spider-grid-outer"
                  : "spider-grid"
              }
              key={ringIndex}
              points={points}
            />
          );
        })}

        {plotted.map((point, index) => {
          if (index % spokeStep !== 0) {
            return null;
          }

          const edge = polarPoint(maximumRadius, index, plotted.length);
          return (
            <line
              className="spider-spoke"
              key={`spoke-${point.generation}-${index}`}
              x1={centerX}
              y1={centerY}
              x2={edge.x}
              y2={edge.y}
            />
          );
        })}

        <polygon className="spider-area-average" points={averagePolygon} />
        <polygon className="spider-area-best" points={bestPolygon} />

        {plotted.map((point, index) => {
          const bestPosition = polarPoint(
            valueRadius(point.best),
            index,
            plotted.length,
          );
          const averagePosition = polarPoint(
            valueRadius(point.average),
            index,
            plotted.length,
          );

          return (
            <g key={`sample-${point.generation}-${index}`}>
              <circle
                className="spider-point spider-point-average"
                cx={averagePosition.x}
                cy={averagePosition.y}
                r="2.4"
              >
                <title>
                  Generación {point.generation}: promedio {formatValue(point.average)}
                </title>
              </circle>
              <circle
                className="spider-point spider-point-best"
                cx={bestPosition.x}
                cy={bestPosition.y}
                r="2.8"
              >
                <title>
                  Generación {point.generation}: mejor {formatValue(point.best)}
                </title>
              </circle>
            </g>
          );
        })}

        {plotted.map((point, index) => {
          if (index % labelStep !== 0 && index !== plotted.length - 1) {
            return null;
          }

          const labelPosition = polarPoint(
            maximumRadius + 28,
            index,
            plotted.length,
          );
          return (
            <text
              className="spider-label"
              dominantBaseline="middle"
              key={`label-${point.generation}-${index}`}
              textAnchor="middle"
              x={labelPosition.x}
              y={labelPosition.y}
            >
              G{point.generation}
            </text>
          );
        })}

        <circle className="spider-center" cx={centerX} cy={centerY} r="4" />
      </svg>

      <div className="chart-caption">
        <span>
          {sampled.length} de {data.length} puntos · muestreo uniforme
        </span>
        <span>
          Rango {formatValue(minY)} – {formatValue(maxY)}
        </span>
      </div>
    </section>
  );
}


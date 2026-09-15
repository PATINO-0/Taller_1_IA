type RouteMapProps = {
  route: number[];
  coordinates: number[][];
};

export function RouteMap({ route, coordinates }: RouteMapProps) {
  if (!route.length || !coordinates.length) {
    return null;
  }

  const width = 720;
  const height = 440;
  const padding = 42;
  const xs = coordinates.map((point) => point[0]);
  const ys = coordinates.map((point) => point[1]);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  const transform = ([x, y]: number[]) => {
    const px =
      padding +
      ((x - minX) / Math.max(1, maxX - minX)) * (width - padding * 2);
    const py =
      height -
      padding -
      ((y - minY) / Math.max(1, maxY - minY)) * (height - padding * 2);
    return [px, py];
  };

  const polyline = route
    .map((city) => transform(coordinates[city]).join(","))
    .join(" ");

  return (
    <svg
      className="route-map"
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label="Ruta del agente viajero"
    >
      <polyline points={polyline} fill="none" className="route-line" />

      {coordinates.map((coordinate, city) => {
        const [x, y] = transform(coordinate);

        return (
          <g key={city}>
            <circle cx={x} cy={y} r="15" className="city-node" />
            <text x={x} y={y + 5} textAnchor="middle" className="city-label">
              {city}
            </text>
          </g>
        );
      })}
    </svg>
  );
}


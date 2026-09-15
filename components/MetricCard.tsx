type MetricCardProps = {
  label: string;
  value: string | number;
  help?: string;
};

export function MetricCard({ label, value, help }: MetricCardProps) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {help ? <small>{help}</small> : null}
    </article>
  );
}


type MetricCardProps = {
  label: string;
  value: string | number;
};

export default function MetricCard({ label, value }: MetricCardProps) {
  return (
    <article>
      <h2>{label}</h2>
      <p>{value}</p>
    </article>
  );
}


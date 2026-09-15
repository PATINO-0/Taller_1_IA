import Link from "next/link";

const problems = [
  {
    href: "/n-queens",
    label: "Problema 01",
    title: "N-Reinas",
    text: "Minimiza conflictos diagonales usando cromosomas de permutación, selección por torneo, OX, swap y elitismo.",
  },
  {
    href: "/tsp",
    label: "Problema 02",
    title: "Agente Viajero",
    text: "Busca una ruta cíclica de distancia mínima y compara mutación por intercambio frente a inversión.",
  },
  {
    href: "/scheduling",
    label: "Problema 03",
    title: "Asignación de cursos",
    text: "Minimiza colisiones, sobrecupo, falta de recursos y franjas inválidas, con comparación de elitismo.",
  },
  {
    href: "/knapsack",
    label: "Problema 04",
    title: "Mochila",
    text: "Maximiza valor con cromosomas binarios y compara penalización frente a reparación.",
  },
];

export default function Home() {
  return (
    <div className="page">
      <section className="hero">
        <span className="eyebrow">Taller 1 · Inteligencia Artificial</span>
        <h1>Laboratorio web de algoritmos genéticos.</h1>
        <p>
          Implementación modular para experimentar con representación,
          aptitud, selección, cruzamiento, mutación, elitismo y criterios de
          parada en cuatro problemas clásicos de búsqueda y optimización.
        </p>
        <div className="hero-actions">
          <Link className="button" href="/n-queens">
            Iniciar experimentos
          </Link>
          <Link className="button secondary" href="/theory">
            Ver fundamentos
          </Link>
        </div>
      </section>

      <section className="problem-grid">
        {problems.map((problem) => (
          <Link className="problem-card" href={problem.href} key={problem.href}>
            <strong>{problem.label}</strong>
            <h2>{problem.title}</h2>
            <p>{problem.text}</p>
          </Link>
        ))}
      </section>
    </div>
  );
}


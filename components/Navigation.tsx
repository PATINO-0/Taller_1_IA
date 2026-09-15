import Link from "next/link";

const links = [
  ["/", "Inicio"],
  ["/theory", "Conceptos"],
  ["/n-queens", "N-Reinas"],
  ["/tsp", "TSP"],
  ["/scheduling", "Horarios"],
  ["/knapsack", "Mochila"],
];

export function Navigation() {
  return (
    <header className="topbar">
      <Link className="brand" href="/">
        Taller <span>1</span>
      </Link>

      <nav className="nav-links" aria-label="Navegación principal">
        {links.map(([href, label]) => (
          <Link key={href} href={href}>
            {label}
          </Link>
        ))}
      </nav>
    </header>
  );
}


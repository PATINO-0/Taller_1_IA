export default function TheoryPage() {
  return (
    <div className="page">
      <section className="problem-hero">
        <span className="eyebrow">Marco conceptual</span>
        <h1>Conceptos clave de algoritmos genéticos</h1>
        <p>
          Base teórica utilizada para justificar las decisiones de diseño de
          los cuatro experimentos implementados.
        </p>
      </section>

      <div className="theory-grid">
        <article className="theory-item">
          <h2>1. ¿Qué es un algoritmo genético?</h2>
          <p>
            Es una técnica de búsqueda y optimización inspirada en la evolución
            biológica. Mantiene una población de soluciones candidatas y favorece
            las mejores mediante selección, cruzamiento y mutación. Se considera
            una técnica de Inteligencia Artificial porque permite explorar
            espacios de búsqueda grandes sin enumerar todas las soluciones.
          </p>
        </article>

        <article className="theory-item">
          <h2>2. Elementos principales</h2>
          <p>
            <b>Población:</b> conjunto de soluciones. <b>Individuo:</b> una
            solución. <b>Cromosoma:</b> representación completa. <b>Gen:</b>
            unidad del cromosoma. <b>Selección:</b> elige padres. <b>Cruzamiento:</b>
            combina información. <b>Mutación:</b> introduce variación. <b>Elitismo:</b>
            conserva las mejores soluciones. <b>Función de aptitud:</b> mide la
            calidad del individuo.
          </p>
        </article>

        <article className="theory-item">
          <h2>3. Función de aptitud</h2>
          <p>
            La función de aptitud define qué significa una solución mejor. En
            maximización se buscan valores mayores, como el valor de la mochila.
            En minimización se buscan valores menores, como los conflictos de
            N-Reinas o la distancia del TSP.
          </p>
        </article>

        <article className="theory-item">
          <h2>4. Operadores según representación</h2>
          <p>
            Para permutaciones son apropiados OX, PMX o CX junto con mutaciones
            swap, inversión o inserción. Para cromosomas binarios son adecuados
            cruce de uno o dos puntos, cruce uniforme y mutación bit-flip.
          </p>
        </article>

        <article className="theory-item">
          <h2>5. Tasa de mutación</h2>
          <p>
            Una tasa demasiado baja puede reducir la diversidad y producir
            convergencia prematura. Una tasa demasiado alta puede destruir
            soluciones útiles y acercar el comportamiento a una búsqueda
            aleatoria.
          </p>
        </article>

        <article className="theory-item">
          <h2>Diseño utilizado</h2>
          <div className="inline-list">
            <span>N-Reinas: permutación + OX + swap</span>
            <span>TSP: permutación + OX + swap/inversión</span>
            <span>Horarios: sala/franja + cruce uniforme</span>
            <span>Mochila: binario + un punto + bit-flip</span>
            <span>Selección: torneo</span>
            <span>Elitismo configurable</span>
          </div>
        </article>
      </div>
    </div>
  );
}


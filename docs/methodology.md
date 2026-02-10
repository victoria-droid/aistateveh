# Metodología / Methodology (ES/EN)

## ES — Marco S, A, T, G, C, R
- **S (Estado):** información mínima pero suficiente para decidir.
- **A (Acción):** decisión concreta que el sistema puede tomar.
- **T (Transición):** cómo cambia el estado al ejecutar una acción.
- **G (Validez):** qué significa “solución válida”.
- **C (Coste):** cómo comparas soluciones válidas (qué es “mejor”).
- **R (Restricciones):**
  - **Hard:** si se violan → inválido.
  - **Soft:** se pueden violar con penalización (entra en C).

### Markov test (pasado → resumen)
Si necesitas pasado, no metas histórico crudo: usa resúmenes (rolling, contadores por ventana, in_transit).

### Granularidad
- **S compacto:** mínimo y explicable.
- **S+ enriquecido:** mejor calidad pero más complejidad y datos.

---

## EN — Framework S, A, T, G, C, R
- **S (State):** minimal but sufficient information to decide.
- **A (Action):** concrete decision the system can take.
- **T (Transition):** how state evolves after an action.
- **G (Validity):** what counts as a valid solution.
- **C (Cost):** how you compare valid solutions (“better”).
- **R (Constraints):**
  - **Hard:** violation → invalid.
  - **Soft:** allowed with penalty (in C).

### Markov test (history → summary)
If past matters, avoid raw history: use summaries (rolling stats, window counters, in_transit).

### Granularity
- **Compact S:** minimal and explainable.
- **Enriched S+:** higher quality but higher complexity/data cost.

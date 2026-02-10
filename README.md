# ai-state-cockpit


# ES/EN — AI Decision State Cockpit (Streamlit)

**Demo (Streamlit):** (pega aquí el enlace tras desplegar)  
**Repo (GitHub):** (pega aquí el enlace del repo)

---

## ES — ¿Qué es esto?
Proyecto “CV-ready” que demuestra **formulación de problemas de IA** con el marco **S, A, T, G, C, R** y su traducción a un producto en **Streamlit**.

Enfoque (lo que le importa a negocio y a recruiters):
- **Estados explícitos** (S) y acciones (A)
- **Restricciones hard vs soft** (R) y trazabilidad
- **Transición** (T) y explicación ejecutiva
- Datos sintéticos pequeños (sin PII)

### Casos
- **Caso A — Logística:** ruteo con ventanas + penalización por tardanza  
- **Caso B — Fraude:** approve/review/block con *velocity features* (Markov resúmenes)  
- **Caso C — Reposición:** pedido con MOQ/múltiplos + coste esperado  

> Nota: score/forecast son “demo” deterministas. Siguiente paso: enchufar modelos entrenados.

---

## EN — What is this?
A “CV-ready” project showcasing **AI problem formulation** using **S, A, T, G, C, R** and translating it into a **Streamlit** product.

Focus (what recruiters care about):
- **Explicit states** (S) and actions (A)
- **Hard vs soft constraints** (R) and traceability
- **Transitions** (T) and executive explanations
- Small synthetic data (no PII)

### Cases
- **Case A — Logistics:** routing with time windows + lateness penalty  
- **Case B — Fraud:** approve/review/block with *velocity features* (Markov summaries)  
- **Case C — Replenishment:** order decisions with MOQ/multiples + expected cost  

> Note: score/forecast are deterministic demo functions. Next step: plug in trained models.

---

## Quickstart (local)
```bash
pip install -r requirements.txt
streamlit run app.py

```
Deploy (Streamlit Community Cloud)

Push this repo to GitHub (public)

Streamlit Cloud → New app

Select repo + branch + app.py

Deploy and paste the public URL above


CV bullet (copy/paste)

ES: “Diseñé y desplegué un cockpit de decisión con Streamlit aplicando S,A,T,G,C,R; validación hard/soft; Markov summaries; y trazabilidad explicable.”
EN: “Built and deployed a Streamlit decision cockpit applying S,A,T,G,C,R; hard/soft constraint validation; Markov summaries; and business-facing traceability.”




### `docs/methodology.md` (bilingüe)
```md
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



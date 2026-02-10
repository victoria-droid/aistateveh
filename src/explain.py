from typing import Dict, Any

def explain_es(case_name: str, state: Dict[str, Any], action: Dict[str, Any],
               hard: Dict[str, Any], cost: Dict[str, Any]) -> str:
    return (
        f"**Caso:** {case_name}\n\n"
        f"**Estado (S) clave:** {', '.join(state.keys())}\n\n"
        f"**Acción (A):** {action}\n\n"
        f"**Hard (validez):** {hard.get('ok')} — {hard.get('reasons', [])}\n\n"
        f"**Coste (C):** total={cost.get('total')} (detalle={cost})\n\n"
        "Interpretación: recomendación óptima *dada la formulación*."
    )

def explain_en(case_name: str, state: Dict[str, Any], action: Dict[str, Any],
               hard: Dict[str, Any], cost: Dict[str, Any]) -> str:
    return (
        f"**Case:** {case_name}\n\n"
        f"**Key State (S):** {', '.join(state.keys())}\n\n"
        f"**Action (A):** {action}\n\n"
        f"**Hard constraints:** {hard.get('ok')} — {hard.get('reasons', [])}\n\n"
        f"**Cost (C):** total={cost.get('total')} (breakdown={cost})\n\n"
        "Interpretation: best recommendation *given the formulation*."
    )

from typing import Dict, Any
from .state_schema import ValidationResult, ok, fail, round_to_multiple

def build_state(on_hand: int, in_transit: int, forecast_next: float,
                moq: int, multiple: int, holding_cost: float, stockout_cost: float, order_fixed_cost: float) -> Dict[str, Any]:
    return {
        "on_hand": int(on_hand),
        "in_transit": int(in_transit),           # Markov summary of past orders
        "forecast_next": float(forecast_next),   # inferred signal (later from ML)
        "moq": int(moq),
        "multiple": int(multiple),
        "holding_cost": float(holding_cost),
        "stockout_cost": float(stockout_cost),
        "order_fixed_cost": float(order_fixed_cost),
    }

def apply_constraints(order_qty: int, state: Dict[str, Any]) -> int:
    q = max(0, int(order_qty))
    if q > 0 and state["moq"] > 0 and q < state["moq"]:
        q = state["moq"]
    q = round_to_multiple(q, state["multiple"])
    return q

def validate_hard(state: Dict[str, Any], action: Dict[str, Any]) -> ValidationResult:
    if "order_qty" not in action:
        return fail("order_qty required")
    return ok()

def transition(state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    q = apply_constraints(action["order_qty"], state)
    ns = dict(state)
    ns["in_transit"] += q
    ns["_applied_order_qty"] = q
    return ns

def cost(state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    q = apply_constraints(action["order_qty"], state)
    inv_pos = state["on_hand"] + state["in_transit"] + q
    ending = inv_pos - state["forecast_next"]
    holding = max(0.0, ending) * state["holding_cost"]
    stockout = max(0.0, -ending) * state["stockout_cost"]
    fixed = state["order_fixed_cost"] if q > 0 else 0.0
    total = holding + stockout + fixed
    return {"applied_qty": q, "holding": round(holding,2), "stockout": round(stockout,2),
            "fixed": round(fixed,2), "total": round(total,2)}

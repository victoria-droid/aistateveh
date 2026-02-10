from typing import Dict, Any, List
from .state_schema import ValidationResult, ok, fail

def build_state(vehicle_position: str, current_time_min: int, capacity_remaining: int,
                pending_deliveries: List[Dict[str, Any]], time_slot: str = "mid") -> Dict[str, Any]:
    # time_slot = Markov summary (traffic regime)
    return {
        "vehicle_position": vehicle_position,
        "current_time_min": int(current_time_min),
        "capacity_remaining": int(capacity_remaining),
        "pending_deliveries": pending_deliveries,
        "time_slot": time_slot,
    }

def validate_hard(state: Dict[str, Any], action: Dict[str, Any]) -> ValidationResult:
    reasons = []
    if action.get("next_stop") is None:
        reasons.append("next_stop required")
    if state["capacity_remaining"] < 0:
        reasons.append("capacity_remaining < 0")
    return ok() if not reasons else fail(*reasons)

def transition(state: Dict[str, Any], action: Dict[str, Any], travel_time_fn) -> Dict[str, Any]:
    next_stop = action["next_stop"]
    pos0 = state["vehicle_position"]
    t0 = state["current_time_min"]
    cap0 = state["capacity_remaining"]
    pending = list(state["pending_deliveries"])

    d = next(x for x in pending if x["stop_id"] == next_stop)
    travel = int(travel_time_fn(pos0, next_stop, state["time_slot"]))
    service = int(d["service_min"])
    size = int(d["size"])

    pending_next = [x for x in pending if x["stop_id"] != next_stop]
    return {
        **state,
        "vehicle_position": next_stop,
        "current_time_min": t0 + travel + service,
        "capacity_remaining": cap0 - size,
        "pending_deliveries": pending_next,
    }

def cost(state: Dict[str, Any], action: Dict[str, Any], travel_time_fn,
         alpha_late: float = 2.0, beta_travel: float = 1.0) -> Dict[str, Any]:
    next_stop = action["next_stop"]
    pos0 = state["vehicle_position"]
    t0 = state["current_time_min"]

    d = next(x for x in state["pending_deliveries"] if x["stop_id"] == next_stop)
    travel = float(travel_time_fn(pos0, next_stop, state["time_slot"]))
    arrival = t0 + travel + d["service_min"]
    late = max(0.0, arrival - d["window_end_min"])  # soft by default

    total = beta_travel * travel + alpha_late * late
    return {"travel_min": travel, "late_min": late, "total": round(total, 2)}

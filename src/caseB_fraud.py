from typing import Dict, Any
from .state_schema import ValidationResult, ok, fail

def build_state(amount: float, device_risk: float, account_age_days: int,
                tx_count_5m: int, tx_amount_1h: float,
                review_capacity_remaining: int) -> Dict[str, Any]:
    # Markov summaries: tx_count_5m, tx_amount_1h (velocity)
    return {
        "amount": float(amount),
        "device_risk": float(device_risk),
        "account_age_days": int(account_age_days),
        "tx_count_5m": int(tx_count_5m),
        "tx_amount_1h": float(tx_amount_1h),
        "review_capacity_remaining": int(review_capacity_remaining),
    }

def simple_score(state: Dict[str, Any]) -> float:
    # Deterministic demo score (replace with trained model later)
    score = 0.0
    score += 0.35 * min(1.0, state["device_risk"])
    score += 0.20 * min(1.0, state["tx_count_5m"] / 10.0)
    score += 0.15 * min(1.0, state["tx_amount_1h"] / 500.0)
    score += 0.10 * min(1.0, state["amount"] / 300.0)
    score += 0.20 * (1.0 if state["account_age_days"] < 14 else 0.0)
    return round(min(1.0, score), 3)

def validate_hard(state: Dict[str, Any], action: Dict[str, Any]) -> ValidationResult:
    decision = action.get("decision")
    if decision not in {"approve", "review", "block"}:
        return fail("decision must be approve/review/block")
    if decision == "review" and state["review_capacity_remaining"] <= 0:
        return fail("no review capacity remaining")
    return ok()

def transition(state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    ns = dict(state)
    if action["decision"] == "review":
        ns["review_capacity_remaining"] -= 1
    return ns

def cost(state: Dict[str, Any], action: Dict[str, Any],
         fp_cost: float = 3.0, fn_cost: float = 10.0) -> Dict[str, Any]:
    p_fraud = simple_score(state)
    decision = action["decision"]
    review_cost = 1.0 if decision == "review" else 0.0

    if decision == "block":
        fp = (1 - p_fraud) * fp_cost; fn = 0.0
    elif decision == "approve":
        fp = 0.0; fn = p_fraud * fn_cost
    else:  # review reduces both
        fp = (1 - p_fraud) * (fp_cost * 0.4)
        fn = p_fraud * (fn_cost * 0.4)

    total = fp + fn + review_cost
    return {"score": p_fraud, "fp_expected": round(fp,2), "fn_expected": round(fn,2),
            "review_cost": review_cost, "total": round(total,2)}

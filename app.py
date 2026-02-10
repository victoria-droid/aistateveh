from pathlib import Path
import pandas as pd
import streamlit as st

from src import caseA_logistics, caseB_fraud, caseC_replenishment
from src.explain import explain_es, explain_en

st.set_page_config(page_title="AI State Cockpit", layout="wide")

lang = st.sidebar.selectbox("Idioma / Language", ["ES", "EN"], index=0)
def t(es: str, en: str) -> str: return es if lang == "ES" else en

st.title(t("Cockpit de Estados para Decisión", "Decision State Cockpit"))

page = st.sidebar.radio(
    t("Sección", "Section"),
    [t("Metodología", "Methodology"),
     t("Caso A — Logística", "Case A — Logistics"),
     t("Caso B — Fraude", "Case B — Fraud"),
     t("Caso C — Reposición", "Case C — Replenishment"),
     t("Resumen", "Summary")],
)

DATA = Path("data")
def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name)

# Travel time: Manhattan distance * minutes-step * traffic multiplier (toy)
def travel_time(pos_from: str, pos_to: str, time_slot: str) -> float:
    df = load_csv("caseA_deliveries.csv").set_index("stop_id")
    a = df.loc[pos_from]; b = df.loc[pos_to]
    dist = abs(a["x"]-b["x"]) + abs(a["y"]-b["y"])
    mult = {"low": 0.9, "mid": 1.0, "peak": 1.25}.get(time_slot, 1.0)
    return float(dist * 6 * mult)

if page == t("Metodología", "Methodology"):
    st.markdown(Path("docs/methodology.md").read_text(encoding="utf-8"))

elif page == t("Caso A — Logística", "Case A — Logistics"):
    df = load_csv("caseA_deliveries.csv")
    stops = df["stop_id"].tolist()
    pending = df[df["stop_id"] != "DEPOT"].rename(columns={"window_end_min":"window_end_min"}).to_dict("records")

    c1, c2 = st.columns(2)
    with c1:
        pos = st.selectbox(t("Posición inicial", "Start position"), stops, index=0)
        now = st.number_input(t("Hora actual (min)", "Current time (min)"), min_value=0, value=0, step=5)
        cap = st.number_input(t("Capacidad restante", "Capacity remaining"), min_value=0, value=10, step=1)
        slot = st.selectbox(t("Franja (Markov tráfico)", "Time slot (Markov traffic)"), ["low","mid","peak"], index=1)
    with c2:
        st.dataframe(df[df["stop_id"] != "DEPOT"][["stop_id","window_end_min","service_min","size","priority"]],
                     use_container_width=True)

    state = caseA_logistics.build_state(pos, int(now), int(cap), pending, time_slot=slot)
    st.markdown(t("### Estado (S)", "### State (S)")); st.json(state)

    next_stop = st.selectbox(t("Acción: siguiente parada", "Action: next stop"),
                            [d["stop_id"] for d in pending])
    alpha = st.slider(t("Peso tardanza (soft)", "Lateness weight (soft)"), 0.0, 5.0, 2.0, 0.25)
    action = {"next_stop": next_stop}

    hard = caseA_logistics.validate_hard(state, action)
    cost = caseA_logistics.cost(state, action, travel_time, alpha_late=alpha)
    ns = caseA_logistics.transition(state, action, travel_time)

    st.markdown(t("### Hard + Coste (C)", "### Hard + Cost (C)"))
    st.write({"ok": hard.ok, "reasons": hard.reasons}); st.write(cost)
    st.markdown(t("### Transición (T)", "### Transition (T)")); st.json(ns)

    st.markdown(t("### Explicación", "### Explanation"))
    st.markdown(explain_es("Logística", state, action, {"ok": hard.ok, "reasons": hard.reasons}, cost)
                if lang=="ES" else
                explain_en("Logistics", state, action, {"ok": hard.ok, "reasons": hard.reasons}, cost))

elif page == t("Caso B — Fraude", "Case B — Fraud"):
    df = load_csv("caseB_transactions.csv")
    tx_id = st.selectbox("tx_id", df["tx_id"].tolist())
    r = df[df["tx_id"] == tx_id].iloc[0].to_dict()

    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input("amount", min_value=0.0, value=float(r["amount"]), step=5.0)
        device_risk = st.slider("device_risk", 0.0, 1.0, float(r["device_risk"]), 0.01)
        age = st.number_input("account_age_days", min_value=0, value=int(r["account_age_days"]), step=1)
    with c2:
        c5m = st.number_input("tx_count_5m", min_value=0, value=int(r["tx_count_5m"]), step=1)
        a1h = st.number_input("tx_amount_1h", min_value=0.0, value=float(r["tx_amount_1h"]), step=10.0)
        cap = st.number_input("review_capacity_remaining", min_value=0, value=int(r["review_capacity_remaining"]), step=1)

    state = caseB_fraud.build_state(amount, device_risk, age, c5m, a1h, cap)
    st.markdown(t("### Estado (S)", "### State (S)")); st.json(state)
    st.metric(t("Score (demo)", "Score (demo)"), caseB_fraud.simple_score(state))

    decision = st.selectbox(t("Acción", "Action"), ["approve","review","block"], index=1)
    action = {"decision": decision}
    hard = caseB_fraud.validate_hard(state, action)
    cost = caseB_fraud.cost(state, action)
    ns = caseB_fraud.transition(state, action)

    st.write({"ok": hard.ok, "reasons": hard.reasons}); st.write(cost); st.json(ns)
    st.markdown(explain_es("Fraude", state, action, {"ok": hard.ok, "reasons": hard.reasons}, cost)
                if lang=="ES" else
                explain_en("Fraud", state, action, {"ok": hard.ok, "reasons": hard.reasons}, cost))

elif page == t("Caso C — Reposición", "Case C — Replenishment"):
    df = load_csv("caseC_inventory_scenarios.csv")
    sc = st.selectbox("scenario", df["scenario"].tolist())
    r = df[df["scenario"] == sc].iloc[0].to_dict()

    c1, c2 = st.columns(2)
    with c1:
        on_hand = st.number_input("on_hand", min_value=0, value=int(r["on_hand"]), step=1)
        in_transit = st.number_input("in_transit", min_value=0, value=int(r["in_transit"]), step=1)
        forecast = st.number_input("forecast_next", min_value=0.0, value=float(r["forecast_next"]), step=1.0)
    with c2:
        moq = st.number_input("moq", min_value=0, value=int(r["moq"]), step=1)
        multiple = st.number_input("multiple", min_value=1, value=int(r["multiple"]), step=1)
        holding = st.number_input("holding_cost", min_value=0.0, value=float(r["holding_cost"]), step=0.01)
        stockout = st.number_input("stockout_cost", min_value=0.0, value=float(r["stockout_cost"]), step=0.1)
        fixed = st.number_input("order_fixed_cost", min_value=0.0, value=float(r["order_fixed_cost"]), step=1.0)

    state = caseC_replenishment.build_state(on_hand, in_transit, forecast, moq, multiple, holding, stockout, fixed)
    st.markdown(t("### Estado (S)", "### State (S)")); st.json(state)

    order_qty = st.number_input(t("Acción: pedir", "Action: order"), min_value=0, value=0, step=1)
    action = {"order_qty": int(order_qty)}

    hard = caseC_replenishment.validate_hard(state, action)
    cost = caseC_replenishment.cost(state, action)
    ns = caseC_replenishment.transition(state, action)

    st.write({"ok": hard.ok, "reasons": hard.reasons}); st.write(cost); st.json(ns)
    st.markdown(explain_es("Reposición", state, action, {"ok": hard.ok, "reasons": hard.reasons}, cost)
                if lang=="ES" else
                explain_en("Replenishment", state, action, {"ok": hard.ok, "reasons": hard.reasons}, cost))

else:
    st.markdown(t(
        "Esta demo conecta metodología → implementación: S explícito, A, validación hard (R), coste soft (C), transición (T).",
        "This demo connects methodology → implementation: explicit S, A, hard validation (R), soft cost (C), transition (T)."
    ))

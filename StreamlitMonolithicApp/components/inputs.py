import streamlit as st
from typing import Dict, Any

def profile_form(profile: Dict[str, Any]) -> Dict[str, Any]:
    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            income = st.number_input("Monthly Income ($)", min_value=0.0, value=float(profile.get("income", 0.0)), step=100.0)
            expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, value=float(profile.get("monthly_expenses", 0.0)), step=100.0)
            city = st.selectbox(
                "City",
                [
                    "New York","San Francisco","Los Angeles","Chicago","Houston","Miami","Seattle","Boston","Austin","Denver","Atlanta","Phoenix","Dallas","Washington DC","San Diego"
                ],
                index=0
            )
        with c2:
            risk = st.slider("Risk Tolerance", 1, 10, int(profile.get("risk_tolerance", 5)))
            savings = st.number_input("Existing Savings ($)", min_value=0.0, value=float(profile.get("existing_savings", 0.0)), step=500.0)
            debts = st.number_input("Debts ($)", min_value=0.0, value=float(profile.get("debts", 0.0)), step=500.0)
            target_rate = st.number_input("Target Savings Rate (%)", min_value=0.0, max_value=100.0, value=float(profile.get("savings_rate_target", 20.0)), step=1.0)
        submitted = st.form_submit_button("Update Profile")
    if submitted:
        return {
            "income": float(income),
            "monthly_expenses": float(expenses),
            "city": city,
            "risk_tolerance": int(risk),
            "existing_savings": float(savings),
            "debts": float(debts),
            "savings_rate_target": float(target_rate)
        }
    return {}


def goal_editor(goal: Dict[str, Any] | None = None, key: str = "goal_form") -> Dict[str, Any]:
    goal = goal or {}
    with st.form(key):
        name = st.text_input("Goal name", value=goal.get("name", ""))
        gtype = st.selectbox("Type", ["Retirement","Home","Education","Custom"], index=3)
        target_amount = st.number_input("Target Amount ($)", min_value=0.0, value=float(goal.get("target_amount", 10000.0)), step=500.0)
        current_amount = st.number_input("Current Amount ($)", min_value=0.0, value=float(goal.get("current_amount", 0.0)), step=500.0)
        horizon_years = st.number_input("Horizon (years)", min_value=1.0, value=float(goal.get("horizon_years", 5.0)), step=1.0)
        priority = st.select_slider("Priority", options=["Low","Medium","High"], value=goal.get("priority", "Medium"))
        submitted = st.form_submit_button("Save Goal")
    if submitted:
        return {
            "name": name or gtype,
            "type": gtype,
            "target_amount": float(target_amount),
            "current_amount": float(current_amount),
            "horizon_years": float(horizon_years),
            "priority": priority
        }
    return {}

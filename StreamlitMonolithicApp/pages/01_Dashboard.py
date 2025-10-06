import streamlit as st
from ..components.kpis import kpi_row
from ..utils.calculations import monthly_surplus, savings_rate, emergency_fund_target

st.set_page_config(page_title="FinMate - Dashboard", page_icon="📊", layout="wide")

state = st.session_state.finmate
profile = state["profile"]

surp = monthly_surplus(profile["income"], profile["monthly_expenses"])
rate = savings_rate(profile["income"], surp)
emer_target = emergency_fund_target(profile["monthly_expenses"], profile["risk_tolerance"])

st.header("📊 Dashboard")

kpi_row([
    {"label": "Monthly Surplus", "value": f"${surp:,.0f}", "delta": None},
    {"label": "Savings Rate", "value": f"{rate:.1f}%", "delta": None},
    {"label": "Emergency Fund Target", "value": f"${emer_target:,.0f}", "delta": None}
])

st.subheader("Quick Adjustments")
col1, col2 = st.columns(2)
with col1:
    income = st.number_input("Monthly Income ($)", min_value=0.0, value=float(profile["income"]))
    expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, value=float(profile["monthly_expenses"]))
with col2:
    risk = st.slider("Risk Tolerance (1-10)", 1, 10, int(profile["risk_tolerance"]))
    city = st.selectbox(
        "City",
        [
            "New York","San Francisco","Los Angeles","Chicago","Houston","Miami","Seattle","Boston","Austin","Denver","Atlanta","Phoenix","Dallas","Washington DC","San Diego"
        ],
        index=0
    )

if st.button("Apply Changes"):
    profile.update({"income": float(income), "monthly_expenses": float(expenses), "risk_tolerance": int(risk), "city": city})
    st.success("Profile updated.")

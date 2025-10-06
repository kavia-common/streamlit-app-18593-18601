import io
import streamlit as st
from ..utils.pdf_generator import generate_pdf
from ..utils.calculations import monthly_surplus, savings_rate, emergency_fund_target
from ..utils.recommender import allocation_for_profile

st.set_page_config(page_title="FinMate - Report", page_icon="📄", layout="wide")

state = st.session_state.finmate
profile = state["profile"]
goals = state["goals"]

st.header("📄 Report PDF")

surp = monthly_surplus(profile["income"], profile["monthly_expenses"])
rate = savings_rate(profile["income"], surp)
emer_target = emergency_fund_target(profile["monthly_expenses"], profile["risk_tolerance"])

# Determine a representative horizon for allocation section
horizon = max([g.get("horizon_years", 5.0) for g in goals], default=5.0)
allocation = allocation_for_profile(profile["risk_tolerance"], horizon)

kpis = {
    "Monthly Surplus": f"${surp:,.0f}",
    "Savings Rate": f"{rate:.1f}%",
    "Emergency Fund Target": f"${emer_target:,.0f}"
}

if st.button("Generate PDF"):
    buffer = io.BytesIO()
    generate_pdf(buffer, "FinMate — Personal Finance Report", profile, kpis, allocation, goals)
    buffer.seek(0)
    st.download_button("Download Report", data=buffer, file_name="finmate_report.pdf", mime="application/pdf")
else:
    st.info("Click the button to generate a professional PDF report.")

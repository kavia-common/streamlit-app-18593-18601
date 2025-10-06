import streamlit as st
from ..utils.recommender import allocation_for_profile, split_surplus_across_goals
from ..utils.calculations import monthly_surplus

st.set_page_config(page_title="FinMate - Recommendations", page_icon="🧠", layout="wide")

state = st.session_state.finmate
profile = state["profile"]
goals = state["goals"]

st.header("🧠 Recommendations")

surp = monthly_surplus(profile["income"], profile["monthly_expenses"])

horizon = max([g.get("horizon_years", 5.0) for g in goals], default=5.0)
allocation = allocation_for_profile(profile["risk_tolerance"], horizon)

st.subheader("Asset Allocation")
st.write({k: f"{v}%" for k, v in allocation.items()})

st.subheader("Monthly Saving Split")
split = split_surplus_across_goals(surp, goals)
if not split:
    st.info("No surplus or no goals to allocate towards.")
else:
    for name, amt in split.items():
        st.write(f"{name}: ${amt:,.2f}/mo")

st.caption("Assumptions: simplified expected returns and cost-of-living adjustments. This is not financial advice.")

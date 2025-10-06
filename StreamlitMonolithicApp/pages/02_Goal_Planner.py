import streamlit as st
from ..components.inputs import goal_editor
from ..utils.calculations import required_monthly_saving, feasibility_flag, monthly_surplus

st.set_page_config(page_title="FinMate - Goal Planner", page_icon="🎯", layout="wide")

state = st.session_state.finmate
profile = state["profile"]
goals = state["goals"]

st.header("🎯 Goal Planner")

with st.expander("Add a new goal", expanded=True):
    new_goal = goal_editor(key="new_goal_form")
    if new_goal:
        goals.append(new_goal)
        st.success(f"Added goal: {new_goal['name']}")

if goals:
    st.subheader("Your Goals")
    removal = None
    for i, g in enumerate(goals):
        with st.expander(f"{g['name']} ({g['priority']}) — {g['horizon_years']} years"):
            st.write(f"Target: ${g['target_amount']:,} | Current: ${g['current_amount']:,}")
            st.write(f"Type: {g['type']}")
            updated = goal_editor(goal=g, key=f"edit_goal_{i}")
            if updated:
                goals[i] = updated
                st.success("Goal updated")
            if st.button("Remove", key=f"remove_{i}"):
                removal = i
        # compute requirement
        req = required_monthly_saving(g['target_amount'], g['current_amount'], g['horizon_years'], profile['city'])
        st.caption(f"Required monthly saving for this goal (est.): ${req:,.2f}")
    if removal is not None:
        goals.pop(removal)
        st.info("Goal removed.")
else:
    st.info("No goals yet. Add one above.")

surp = monthly_surplus(profile['income'], profile['monthly_expenses'])
if goals:
    st.subheader("Feasibility Snapshot")
    for g in goals:
        req = required_monthly_saving(g['target_amount'], g['current_amount'], g['horizon_years'], profile['city'])
        flag = feasibility_flag(req, surp)
        st.write(f"{g['name']}: needs ${req:,.2f}/mo — Feasibility: {flag}")

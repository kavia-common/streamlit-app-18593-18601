import streamlit as st
from pathlib import Path
import json

st.set_page_config(page_title="FinMate", page_icon="💹", layout="wide")

DATA_DIR = Path(__file__).parent / ".data"
DATA_DIR.mkdir(exist_ok=True)
PERSIST_FILE = DATA_DIR / "user_profile.json"

DEFAULT_STATE = {
    "profile": {
        "income": 7000.0,
        "monthly_expenses": 4000.0,
        "city": "New York",
        "risk_tolerance": 5,
        "existing_savings": 10000.0,
        "debts": 0.0,
        "savings_rate_target": 20.0
    },
    "goals": [],
    "settings": {"persist_locally": False}
}

if "finmate" not in st.session_state:
    st.session_state.finmate = DEFAULT_STATE.copy()

st.title("💹 FinMate — Personal Finance & Investment Assistant")

with st.expander("About FinMate", expanded=True):
    st.markdown(
        """
        FinMate helps you plan goals, understand your cash flow, and get smart, personalized investment guidance.
        
        How to use:
        - Start at Dashboard to review KPIs and quick inputs.
        - Use Goal Planner to add/edit financial goals with amounts and timelines.
        - See Recommendations for asset allocation and monthly saving targets.
        - Generate a professional PDF report in Report PDF.
        
        Notes: Data is held in your browser session. You can optionally persist it locally as a JSON file.
        """
    )

col1, col2 = st.columns([2,1])
with col1:
    st.subheader("Quick Profile Setup")
    income = st.number_input("Monthly Income ($)", min_value=0.0, value=st.session_state.finmate["profile"]["income"], step=100.0)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, value=st.session_state.finmate["profile"]["monthly_expenses"], step=100.0)
    city = st.selectbox(
        "City",
        [
            "New York","San Francisco","Los Angeles","Chicago","Houston","Miami","Seattle","Boston","Austin","Denver","Atlanta","Phoenix","Dallas","Washington DC","San Diego"
        ],
        index=0
    )
    risk = st.slider("Risk Tolerance (1=Low, 10=High)", 1, 10, int(st.session_state.finmate["profile"]["risk_tolerance"]))
    savings = st.number_input("Existing Savings ($)", min_value=0.0, value=st.session_state.finmate["profile"].get("existing_savings", 0.0), step=500.0)
    debts = st.number_input("Debts ($)", min_value=0.0, value=st.session_state.finmate["profile"].get("debts", 0.0), step=500.0)
    target_rate = st.number_input("Target Savings Rate (%)", min_value=0.0, max_value=100.0, value=st.session_state.finmate["profile"].get("savings_rate_target", 20.0), step=1.0)

    if st.button("Save Profile"):
        st.session_state.finmate["profile"].update({
            "income": float(income),
            "monthly_expenses": float(expenses),
            "city": city,
            "risk_tolerance": int(risk),
            "existing_savings": float(savings),
            "debts": float(debts),
            "savings_rate_target": float(target_rate)
        })
        st.success("Profile saved.")

with col2:
    st.subheader("Persistence")
    persist = st.toggle("Persist locally (.data/user_profile.json)", value=st.session_state.finmate["settings"]["persist_locally"])    
    st.session_state.finmate["settings"]["persist_locally"] = persist
    if st.button("Save to file"):
        with open(PERSIST_FILE, "w") as f:
            json.dump(st.session_state.finmate, f, indent=2)
        st.success(f"Saved to {PERSIST_FILE}")
    if st.button("Load from file"):
        if PERSIST_FILE.exists():
            with open(PERSIST_FILE) as f:
                st.session_state.finmate = json.load(f)
            st.success("Loaded saved profile.")
        else:
            st.info("No saved profile found.")

st.info("Use the sidebar or pages to navigate: Dashboard, Goal Planner, Recommendations, Report PDF.")

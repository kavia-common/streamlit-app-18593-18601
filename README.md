# streamlit-app-18593-18601

This workspace hosts the FinMate Streamlit monolithic app.

Quick start:
- Install: `pip install -r StreamlitMonolithicApp/requirements.txt`
- Run: `streamlit run StreamlitMonolithicApp/app.py --server.port 3000 --server.address 0.0.0.0`
- Open: http://localhost:3000

For full details, see the README at StreamlitMonolithicApp/README.md or below.

# FinMate — Streamlit Personal Finance App

FinMate analyzes income, city, and goals to offer personalized investment advice. It features an interactive UI, charts, and professional PDF report generation.

## Run locally

1. Create and activate a virtual environment (recommended)
```
python -m venv .venv
. .venv/bin/activate
```

2. Install dependencies
```
pip install -r StreamlitMonolithicApp/requirements.txt
```

3. Start app on port 3000
```
streamlit run StreamlitMonolithicApp/app.py --server.port 3000 --server.address 0.0.0.0
```

Then open http://localhost:3000 in your browser.

## Structure
- StreamlitMonolithicApp/app.py — Home, session state, persistence
- pages/01_Dashboard.py — KPIs and quick adjustments
- pages/02_Goal_Planner.py — CRUD goals and feasibility
- pages/03_Recommendations.py — Allocation and monthly split
- pages/04_Report_PDF.py — PDF generation
- components/ — inputs, KPIs, charts
- utils/ — data models, calculations, recommender, PDF, datasets loaders
- assets/ — CSVs for COL and expected returns

## Notes
- No external paid APIs
- Data persisted in session; optional local JSON save in .data/
- This is not financial advice

#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="/home/kavia/workspace/code-generation/streamlit-app-18593-18601/StreamlitMonolithicApp"
cd "$WORKSPACE"
# requirements: conservative pin, editable by developer
if [ ! -f requirements.txt ]; then cat > requirements.txt <<'REQ'
streamlit~=1.30.0
pytest>=7.0.0
REQ
fi
# Minimal Streamlit app (do not overwrite existing)
if [ ! -f app.py ]; then cat > app.py <<'PY'
import os
import streamlit as st
st.title('StreamlitMonolithicApp - Dev Scaffold')
st.write('Workspace:', os.getcwd())
if not os.path.exists('data'):
    os.makedirs('data')
st.write('Data dir exists:', os.path.exists('data'))
PY
fi
# Create minimal SQLite placeholder
mkdir -p data && touch data/app.db
# README shows venv usage to be explicit for automation
if [ ! -f README.md ]; then cat > README.md <<'MD'
Minimal Streamlit scaffold.
Run with workspace venv:
  source .venv/bin/activate && streamlit run app.py --server.headless true --server.port 8501
Or without activation (explicit path):
  ./.venv/bin/streamlit run app.py --server.headless true --server.port 8501
MD
fi

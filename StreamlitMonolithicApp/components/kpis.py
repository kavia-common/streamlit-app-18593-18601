import streamlit as st

def kpi_card(label: str, value: str, delta: str | None = None, help_text: str | None = None):
    st.metric(label=label, value=value, delta=delta, help=help_text)


def kpi_row(items):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            kpi_card(**item)

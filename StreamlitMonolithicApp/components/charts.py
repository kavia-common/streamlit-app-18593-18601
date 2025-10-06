import io
from typing import Dict, List
import plotly.express as px
import pandas as pd

def allocation_pie(allocation: Dict[str, float]):
    labels = list(allocation.keys())
    values = list(allocation.values())
    fig = px.pie(values=values, names=labels, title="Recommended Allocation")
    return fig

def savings_over_time(monthly_saving: float, months: int = 60):
    df = pd.DataFrame({
        "Month": list(range(1, months + 1)),
        "Cumulative Savings": [monthly_saving * m for m in range(1, months + 1)]
    })
    fig = px.line(df, x="Month", y="Cumulative Savings", title="Savings Projection (no returns)")
    return fig

def fig_to_png_bytes(fig):
    buf = io.BytesIO()
    # Note: exporting static image requires kaleido; if not installed, caller should avoid using this function.
    fig.write_image(buf, format="png")
    buf.seek(0)
    return buf.read()

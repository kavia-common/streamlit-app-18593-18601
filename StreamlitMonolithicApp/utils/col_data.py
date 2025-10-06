import pandas as pd
from pathlib import Path

ASSET_PATH = Path(__file__).parent.parent / "assets" / "sample_col_indices.csv"

CITY_DEFAULT = 100.0

def load_col_index():
    try:
        df = pd.read_csv(ASSET_PATH)
        return df
    except Exception:
        return pd.DataFrame({"city": ["Default"], "col_index": [CITY_DEFAULT]})

def get_city_col(city: str) -> float:
    df = load_col_index()
    row = df[df["city"] == city]
    if row.empty:
        return CITY_DEFAULT
    return float(row.iloc[0]["col_index"])

import pandas as pd
from pathlib import Path

ASSET_PATH = Path(__file__).parent.parent / "assets" / "sample_expected_returns.csv"

DEFAULT_RETURNS = {
    "Equities": {"exp_return": 0.07, "vol": 0.15},
    "Bonds": {"exp_return": 0.03, "vol": 0.05},
    "REITs": {"exp_return": 0.06, "vol": 0.12},
    "Gold": {"exp_return": 0.02, "vol": 0.10},
    "Cash": {"exp_return": 0.01, "vol": 0.01}
}

def load_expected_returns():
    try:
        df = pd.read_csv(ASSET_PATH)
        return df
    except Exception:
        return pd.DataFrame([
            {"asset": k, "exp_return": v["exp_return"], "vol": v["vol"]}
            for k, v in DEFAULT_RETURNS.items()
        ])

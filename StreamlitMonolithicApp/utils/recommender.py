from typing import List, Dict
from .calculations import risk_capacity

ALLOCATION_TABLE = [
    (0.0, {"Cash": 80, "Bonds": 20}),
    (0.25, {"Cash": 40, "Bonds": 50, "Equities": 10}),
    (0.5, {"Cash": 15, "Bonds": 45, "Equities": 30, "REITs": 10}),
    (0.75, {"Cash": 5, "Bonds": 25, "Equities": 55, "REITs": 10, "Gold": 5}),
    (1.01, {"Cash": 2, "Bonds": 18, "Equities": 65, "REITs": 10, "Gold": 5})
]

def allocation_for_profile(risk_tolerance: int, horizon_years: float) -> Dict[str, float]:
    score = risk_capacity(risk_tolerance, horizon_years)
    chosen = ALLOCATION_TABLE[0][1]
    for threshold, alloc in ALLOCATION_TABLE:
        if score >= threshold:
            chosen = alloc
    # normalize to 100
    total = sum(chosen.values())
    return {k: round(v * 100.0 / total, 2) for k, v in chosen.items()}

def split_surplus_across_goals(monthly_surplus: float, goals: List[Dict]) -> Dict[str, float]:
    if monthly_surplus <= 0 or not goals:
        return {}
    # Priority weights: High 3, Medium 2, Low 1; shorter horizon slightly higher weight
    priority_map = {"High": 3, "Medium": 2, "Low": 1}
    weights = []
    for g in goals:
        w = priority_map.get(g.get("priority", "Medium"), 2) * (1 + 1.0 / max(1.0, g.get("horizon_years", 5.0)))
        weights.append(max(0.1, w))
    wsum = sum(weights)
    return {g.get("name", f"Goal {i+1}"): round((w / wsum) * monthly_surplus, 2) for i, (g, w) in enumerate(zip(goals, weights))}

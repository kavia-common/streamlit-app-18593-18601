from typing import List, Dict
import math
from .col_data import get_city_col

def monthly_surplus(income: float, expenses: float) -> float:
    return max(0.0, income - expenses)

def savings_rate(income: float, surplus: float) -> float:
    if income <= 0:
        return 0.0
    return (surplus / income) * 100.0

def emergency_fund_target(expenses: float, risk_tolerance: int) -> float:
    months = 6 if risk_tolerance <= 3 else 4 if risk_tolerance <= 7 else 3
    return expenses * months

def required_monthly_saving(target_amount: float, current_amount: float, horizon_years: float, city: str, real_return: float = 0.03) -> float:
    # Adjust target by cost-of-living index (city relative to 100)
    col_idx = get_city_col(city)
    adjusted_target = target_amount * (col_idx / 100.0)
    n = int(horizon_years * 12)
    pv = current_amount
    r = real_return / 12.0
    # Solve for PMT in future value of annuity: FV = PV*(1+r)^n + PMT*(((1+r)^n -1)/r)
    fv_needed = max(0.0, adjusted_target - pv * (1 + r) ** n)
    if n <= 0:
        return max(0.0, fv_needed)
    if r == 0:
        return fv_needed / n
    annuity_factor = ((1 + r) ** n - 1) / r
    return fv_needed / annuity_factor

def risk_capacity(risk_tolerance: int, horizon_years: float) -> float:
    # Simple blend, scaled 0-1
    rt = max(1, min(10, risk_tolerance)) / 10.0
    hz = min(30.0, max(1.0, horizon_years)) / 30.0
    return 0.6 * rt + 0.4 * hz

def feasibility_flag(monthly_required: float, available: float) -> str:
    if monthly_required <= 0.8 * available:
        return "Green"
    if monthly_required <= 1.2 * available:
        return "Yellow"
    return "Red"

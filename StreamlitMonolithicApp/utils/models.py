from typing import List, Literal, Dict, Any
from pydantic import BaseModel, Field

class Goal(BaseModel):
    name: str
    type: Literal["Retirement","Home","Education","Custom"] = "Custom"
    target_amount: float
    current_amount: float = 0.0
    horizon_years: float
    priority: Literal["Low","Medium","High"] = "Medium"

class UserProfile(BaseModel):
    income: float
    monthly_expenses: float
    city: str
    risk_tolerance: int = Field(ge=1, le=10)
    existing_savings: float = 0.0
    debts: float = 0.0
    savings_rate_target: float = 20.0

class DerivedState(BaseModel):
    monthly_surplus: float
    savings_rate_actual: float
    emergency_fund_target: float
    emergency_fund_current: float

class AppState(BaseModel):
    profile: UserProfile
    goals: List[Goal] = []
    settings: Dict[str, Any] = {"persist_locally": False}

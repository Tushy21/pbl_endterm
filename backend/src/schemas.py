# backend/src/schemas.py

from pydantic import BaseModel


# ---------------------------------------------------------
# Input Schema (Request Body)
# ---------------------------------------------------------

class LoanApplication(BaseModel):
    loan_amnt: float
    annual_inc: float
    dti: float
    revol_bal: float
    total_acc: float


# ---------------------------------------------------------
# Prediction Response Schema
# ---------------------------------------------------------

class PredictionResponse(BaseModel):
    probability_default: float
    prediction: int
    risk_level: str


# ---------------------------------------------------------
# SHAP Explanation Schema (Optional - For /explain)
# ---------------------------------------------------------

class FeatureContribution(BaseModel):
    feature: str
    contribution: float


class ExplanationResponse(BaseModel):
    probability_default: float
    top_contributing_features: list[FeatureContribution]

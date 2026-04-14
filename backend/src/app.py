from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import LoanApplication, PredictionResponse, ExplanationResponse
from src.explainer import get_explanation
from src.model_loader import get_model
import pandas as pd

app = FastAPI(title="Credit Risk Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "API Running"}

@app.post("/api/predict", response_model=PredictionResponse)
def predict(data: LoanApplication):

    pipeline = get_model()  # This is a dict

    preprocessor = pipeline["preprocessor"]
    model = pipeline["model"]

    input_df = pd.DataFrame([data.dict()])

    X_processed = preprocessor.transform(input_df)

    probability = model.predict_proba(X_processed)[0][1]
    prediction = int(probability > 0.5)

    if probability > 0.15:
        risk = "High"
    elif probability > 0.08:
        risk = "Medium"
    else:
        risk = "Low"


    return {
        "probability_default": float(probability),
        "prediction": prediction,
        "risk_level": risk
    }

@app.post("/api/explain", response_model=ExplanationResponse)
def explain(data: LoanApplication):
    pipeline = get_model()
    input_df = pd.DataFrame([data.dict()])
    
    # Get standard prediction probability to include in response
    preprocessor = pipeline["preprocessor"]
    model = pipeline["model"]
    X_processed = preprocessor.transform(input_df)
    probability = float(model.predict_proba(X_processed)[0][1])
    
    # Get SHAP contributions
    contributions = get_explanation(pipeline, input_df)
    
    return {
        "probability_default": probability,
        "top_contributing_features": contributions
    }

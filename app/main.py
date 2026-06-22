from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# ── Load Model Artifacts ──
model         = joblib.load('model/churn_model.pkl')
scaler        = joblib.load('model/scaler.pkl')
feature_names = joblib.load('model/feature_names.pkl')

app = FastAPI(title="ConnectTel Churn Prediction API")

# ── Input Schema ──
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    gender: int
    Partner: int
    Dependents: int
    PhoneService: int
    PaperlessBilling: int
    SeniorCitizen: int

# ── Health Check ──
@app.get("/health")
def health():
    return {"status": "OK", "model": "ConnectTel Churn Predictor"}

# ── Predict Endpoint ──
@app.post("/predict")
def predict(data: CustomerData):
    # Create input dataframe
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])

    # Add missing features with 0
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder columns
    input_df = input_df[feature_names]

    # Scale numerical features
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges',
                'AvgMonthlySpend', 'ChargesRatio']
    for col in num_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    # Predict
    proba = model.predict_proba(input_df)[0][1]
    prediction = int(proba >= 0.5)

    return {
        "churn_prediction": prediction,
        "churn_probability": round(float(proba), 4),
        "risk_level": "High" if proba >= 0.7 else "Medium" if proba >= 0.4 else "Low",
        "message": "Customer likely to churn!" if prediction == 1 else "Customer likely to stay!"
    }

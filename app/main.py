from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os

# ── Load Model Artifacts ──
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model         = joblib.load(os.path.join(BASE_DIR, 'model', 'churn_model.pkl'))
scaler        = joblib.load(os.path.join(BASE_DIR, 'model', 'scaler.pkl'))
feature_names = joblib.load(os.path.join(BASE_DIR, 'model', 'feature_names.pkl'))

app = FastAPI(title="ConnectTel Churn Prediction API")

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

@app.get("/health")
def health():
    return {"status": "OK", "model": "ConnectTel Churn Predictor"}

@app.post("/predict")
def predict(data: CustomerData):
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])

    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[feature_names]

    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges',
                'AvgMonthlySpend', 'ChargesRatio']
    for col in num_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    proba = model.predict_proba(input_df)[0][1]
    prediction = int(proba >= 0.5)

    return {
        "churn_prediction": prediction,
        "churn_probability": round(float(proba), 4),
        "risk_level": "High" if proba >= 0.7 else "Medium" if proba >= 0.4 else "Low",
        "message": "Customer likely to churn!" if prediction == 1 else "Customer likely to stay!"
    }

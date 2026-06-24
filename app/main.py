from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="ConnectTel Churn Predictor")

# Load model files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, "model/churn_model.pkl"))
preprocessor = joblib.load(os.path.join(BASE_DIR, "model/preprocessor.pkl"))
feature_names = joblib.load(os.path.join(BASE_DIR, "model/feature_names.pkl"))

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: CustomerData):
    import pandas as pd
    input_dict = data.dict()
    df = pd.DataFrame([input_dict])
    
    # Encode using saved encoders
    for col in df.select_dtypes('object').columns:
        if col in preprocessor:
            le = preprocessor[col]
            df[col] = le.transform(df[col])
    
    df = df[feature_names]
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return {
        "churn_prediction": int(prediction),
        "churn_label": "Yes" if prediction == 1 else "No",
        "churn_probability": round(float(probability), 3)
    }

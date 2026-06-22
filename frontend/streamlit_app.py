import streamlit as st
import requests

# ── Page Config ──
st.set_page_config(
    page_title="ConnectTel Churn Predictor",
    page_icon="📡",
    layout="centered"
)

# ── Header ──
st.title("📡 ConnectTel Customer Churn Predictor")
st.markdown("Enter customer details below to predict churn risk.")
st.divider()

# ── Input Form ──
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0)
    total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 500.0)
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])

with col2:
    partner = st.selectbox("Has Partner", ["No", "Yes"])
    dependents = st.selectbox("Has Dependents", ["No", "Yes"])
    phone_service = st.selectbox("Phone Service", ["No", "Yes"])
    paperless = st.selectbox("Paperless Billing", ["No", "Yes"])

st.divider()

# ── Predict Button ──
if st.button("🔮 Predict Churn", use_container_width=True):
    payload = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "gender": 1 if gender == "Male" else 0,
        "Partner": 1 if partner == "Yes" else 0,
        "Dependents": 1 if dependents == "Yes" else 0,
        "PhoneService": 1 if phone_service == "Yes" else 0,
        "PaperlessBilling": 1 if paperless == "Yes" else 0,
        "SeniorCitizen": 1 if senior == "Yes" else 0
    }

    try:
        API_URL = "http://localhost:8000/predict"
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.divider()

        # ── Results ──
        risk = result['risk_level']
        prob = result['churn_probability'] * 100

        if risk == "High":
            st.error(f"🚨 HIGH RISK — {prob:.1f}% Churn Probability")
        elif risk == "Medium":
            st.warning(f"⚠️ MEDIUM RISK — {prob:.1f}% Churn Probability")
        else:
            st.success(f"✅ LOW RISK — {prob:.1f}% Churn Probability")

        col1, col2, col3 = st.columns(3)
        col1.metric("Prediction", "Will Churn" if result['churn_prediction'] == 1 else "Will Stay")
        col2.metric("Probability", f"{prob:.1f}%")
        col3.metric("Risk Level", risk)

        st.info(f"💡 {result['message']}")

    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        st.info("Make sure the FastAPI backend is running!")

# ── Footer ──
st.divider()
st.caption("ConnectTel Churn Predictor | Persevex AI Internship | Harbhajan Singh Guru")

import streamlit as st
import requests

st.set_page_config(page_title="ConnectTel Churn Predictor", page_icon="📡")

st.title("📡 ConnectTel Customer Churn Predictor")
st.markdown("Fill in customer details to predict churn probability.")

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
    MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

with col2:
    InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

with col3:
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
    PaymentMethod = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])
    MonthlyCharges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0)
    TotalCharges = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0)

if st.button("🔍 Predict Churn", use_container_width=True):
    payload = {
        "gender": gender, "SeniorCitizen": SeniorCitizen,
        "Partner": Partner, "Dependents": Dependents,
        "tenure": tenure, "PhoneService": PhoneService,
        "MultipleLines": MultipleLines, "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity, "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection, "TechSupport": TechSupport,
        "StreamingTV": StreamingTV, "StreamingMovies": StreamingMovies,
        "Contract": Contract, "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod, "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }
    try:
        response = requests.post("https://connecttel-churn-app-1.onrender.com/predict", json=payload)
        result = response.json()
        if result["churn_label"] == "Yes":
            st.error(f"⚠️ Customer likely to CHURN! Probability: {result['churn_probability']*100:.1f}%")
        else:
            st.success(f"✅ Customer likely to STAY! Probability: {(1-result['churn_probability'])*100:.1f}%")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

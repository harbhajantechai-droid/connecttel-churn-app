# 📡 ConnectTel Customer Churn Predictor

A production-ready ML application that predicts customer churn using Random Forest Classifier, deployed with FastAPI + Streamlit + Docker.

## 🔗 Live Application
**URL:** https://connecttel-churn-app-1.onrender.com

## 🏗️ Project Structure
```
connecttel-churn-app/
├── app/
│   └── main.py             # FastAPI backend
├── frontend/
│   └── streamlit_app.py    # Streamlit UI
├── model/
│   ├── churn_model.pkl     # Trained model
│   ├── preprocessor.pkl    # Label encoders
│   └── feature_names.pkl   # Feature list
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🚀 API Endpoints

**GET /health** — Check if app is running
```
Response: {"status": "ok"}
```

**POST /predict** — Predict customer churn
```
Input: Customer details (JSON)
Output: {"churn_prediction": 0, "churn_label": "No", "churn_probability": 0.15}
```

## 🛠️ Tech Stack
- ML Model: RandomForestClassifier (79.2% accuracy)
- Backend: FastAPI + Uvicorn
- Frontend: Streamlit
- Container: Docker
- Deployment: Render.com
- Dataset: IBM Telco Customer Churn

## 🏃 Run Locally
```bash
docker build -t connecttel-churn .
docker run -p 8501:8501 connecttel-churn
```

## 👨‍💻 Author
**Harbhajan Singh Guru**
AI/ML Intern @ Persevex
harbhajan.tech.ai@gmail.com
[LinkedIn](https://linkedin.com/in/harbhajan-guru)

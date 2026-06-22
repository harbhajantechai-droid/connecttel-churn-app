# ── Base Image — Match Colab Python Version ──
FROM python:3.10.12-slim

# ── Set Working Directory ──
WORKDIR /app

# ── Copy All Files ──
COPY . .

# ── Install Dependencies ──
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    pydantic==2.4.2 \
    joblib==1.3.2 \
    numpy==1.24.3 \
    pandas==2.0.3 \
    scikit-learn==1.3.2 \
    xgboost==2.0.3

# ── Expose Port ──
EXPOSE 8000

# ── Run FastAPI Server ──
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

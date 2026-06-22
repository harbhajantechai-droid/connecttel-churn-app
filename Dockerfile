# ── Base Image ──
FROM python:3.10-slim

# ── Set Working Directory ──
WORKDIR /app

# ── Copy All Files ──
COPY . .

# ── Install Dependencies ──
RUN pip install --no-cache-dir -r requirements.txt

# ── Expose Port ──
EXPOSE 8000

# ── Run FastAPI Server ──
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

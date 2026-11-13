# ---------- Stage 1: build the React frontend ----------
FROM node:22-slim AS frontend-build
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
# VITE_API_URL is unset, so the app calls /api on the same origin
RUN npm run build

# ---------- Stage 2: Python API + built frontend ----------
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8000

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY app ./app
COPY data ./data
COPY models ./models
COPY --from=frontend-build /build/dist ./frontend/dist

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.api.server:app --host 0.0.0.0 --port ${PORT:-8000}"]

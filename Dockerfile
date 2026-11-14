# ---------- Stage 1: build the React frontend ----------
FROM node:22-slim AS frontend-build
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---------- Stage 2: Python API + built frontend ----------
FROM python:3.12-slim

# Hugging Face Spaces runs containers as user 1000
RUN useradd -m -u 1000 user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 \
    TF_CPP_MIN_LOG_LEVEL=2 PORT=7860
WORKDIR /home/user/app

COPY --chown=user requirements-prod.txt .
USER user
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY --chown=user app ./app
COPY --chown=user data ./data
COPY --chown=user models ./models
COPY --chown=user --from=frontend-build /build/dist ./frontend/dist

EXPOSE 7860
CMD ["sh", "-c", "uvicorn app.api.server:app --host 0.0.0.0 --port ${PORT:-7860}"]

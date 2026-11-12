# FinAgent — Deployment & Execution Guide

## Quick Start (Run Locally)

### Option A: 1-Click Launch (Windows)
Double click `run.bat` or run in terminal:
```cmd
python main.py
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser!

### Option B: Frontend Hot-Reload Development
If you want to edit React components live:
1. Terminal 1 (Backend API):
   ```cmd
   python main.py
   ```
2. Terminal 2 (Vite Frontend):
   ```cmd
   cd frontend
   npm run dev
   ```
   Open **[http://localhost:5173](http://localhost:5173)**. All `/api` requests are automatically proxied to port 8000.

---

## Cloud Deployment (Docker / Render / Railway)

### Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy project files
COPY . .

# Expose port and launch
EXPOSE 8000
CMD ["uvicorn", "app.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Render / Railway (Procfile)
```procfile
web: uvicorn app.api.server:app --host 0.0.0.0 --port $PORT
```

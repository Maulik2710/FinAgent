# Deploy FinAgent (one service: API + React UI)

1. Copy these 4 files into the project ROOT (next to main.py), replacing the old ones:
   Dockerfile, requirements-prod.txt, .dockerignore, render.yaml
2. Test locally (optional but recommended):
   docker build -t finagent .
   docker run -p 8000:8000 -e GEMINI_API_KEY=xxx -e NEWS_API_KEY=xxx finagent
   -> open http://localhost:8000
3. git add . && git commit -m "Docker deploy" && git push
4. Render: New + > Blueprint (or Web Service > Docker) > pick the repo.
   Add env vars GEMINI_API_KEY and NEWS_API_KEY in the dashboard.
5. Open the .onrender.com URL.

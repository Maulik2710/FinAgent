# Deploy FinAgent on Hugging Face Spaces

1. Create account at huggingface.co, then New > Space.
   - Name: finagent   - SDK: Docker (Blank)   - Hardware: CPU basic (free)   - Visibility: Public
2. Add secrets: Space > Settings > Variables and secrets > "New secret"
   GEMINI_API_KEY and NEWS_API_KEY  (use a NEW Gemini key)
3. Copy Dockerfile, README.md, requirements-prod.txt, .dockerignore into your project root
   (README.md must be in the ROOT, replacing nothing - you have no root README).
4. Push your project to the Space. Use a fresh single-commit history so old commits with
   binary files (.keras/.pkl/.faiss/.png) don't get rejected:
   git lfs install
   git lfs track "*.keras" "*.pkl" "*.faiss" "*.png"
   git remote add space https://huggingface.co/spaces/<USERNAME>/finagent
   git checkout --orphan hf-deploy
   git add -A
   git commit -m "Deploy to HF Spaces"
   git push space hf-deploy:main --force
   (username = your HF username, password = a HF access token with Write permission)
   Then switch back to your normal branch: git checkout main
5. Watch the Logs tab on the Space; when it says Running, your app is live at
   https://<USERNAME>-finagent.hf.space

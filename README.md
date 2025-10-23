# Cleaned NLP Query Engine (Demo)

This is a cleaned, runnable demo version of your NLP Query Engine project.

## How to run (backend)
1. Create a Python virtualenv and install requirements:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start the backend:
   ```
   uvicorn backend.main:app --reload --port 8000
   ```
3. Open the demo UI:
   Visit http://localhost:8000/frontend/public/index.html
   (or copy `frontend/public/index.html` into a simple static server)

## Notes
- This demo intentionally disables arbitrary SQL execution for safety.
- Document semantic search uses simple keyword matching over processed chunks stored in `data/embeddings`.
- Schema discovery uses SQLAlchemy inspector and works with SQLite, Postgres, MySQL connection strings.

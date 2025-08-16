1. Duplicate `.env.example` -> `.env` and fill values
2. Start postgres (docker-compose or local)
3. Install deps: `pip install -r requirements.txt`
4. Run alembic migrations or let the app create tables on startup (dev only)
5. Start server: `uvicorn app.main:app --reload`
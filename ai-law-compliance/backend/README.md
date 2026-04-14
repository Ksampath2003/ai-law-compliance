# Backend — FastAPI

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # edit .env with your keys
```

## Database

```bash
# Run migrations
alembic upgrade head

# Seed sample laws (8 real U.S. AI laws)
python scripts/seed_laws.py
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

Docs: http://localhost:8000/docs

## Ingest Custom Laws

Create a JSON file following this format:

```json
[
  {
    "title": "Example State AI Transparency Act",
    "state": "XX",
    "summary": "Requires companies using AI...",
    "full_text": "Full legislative text...",
    "status": "pending",
    "effective_date": "2026-01-01",
    "ai_category": "LLM",
    "industries_affected": ["technology", "healthcare"],
    "risk_level": "high",
    "compliance_steps": ["Step 1", "Step 2"],
    "source_url": "https://..."
  }
]
```

Then run:
```bash
python scripts/ingest_laws.py --file your_laws.json
```

## Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/laws` | List laws (filter by state, status, risk) |
| GET | `/api/laws/{id}` | Law detail |
| GET | `/api/laws/state/{state}` | Laws by state |
| POST | `/api/compliance/analyze` | Compliance analysis |
| POST | `/api/search` | Semantic search |
| POST | `/api/ingest` | Ingest new laws (requires admin key) |

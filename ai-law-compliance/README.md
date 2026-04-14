# ⚖️ AI Law Compliance Assistant

An AI-powered tool that tracks, explains, and helps companies comply with **AI-specific legislation** across all U.S. states — filtering out general privacy laws to focus only on what matters for AI teams.

---

## ✨ Features

- 🔍 **AI-only filtering** — Only ingests laws explicitly about AI, ML, generative AI, or automated decision systems
- 📋 **Plain-English summaries** — LLM-generated explanations of complex legislation
- ✅ **Compliance checklists** — Actionable steps tailored to your industry and AI usage
- 🚦 **Risk scoring** — High / Medium / Low risk per law
- 📡 **Live + Pending tracking** — See what's active and what's coming
- 🔎 **Semantic search** — Find relevant laws by describing your use case

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                │
│         Tailwind CSS + shadcn/ui components          │
└──────────────────────┬──────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────┐
│                 Backend (FastAPI)                    │
│   /laws  /search  /compliance  /analyze  /ingest    │
└────────┬──────────────────────┬────────────────────┘
         │                      │
┌────────▼────────┐   ┌─────────▼──────────┐
│   PostgreSQL    │   │  Pinecone / Chroma  │
│  (law records)  │   │  (vector search)    │
└─────────────────┘   └────────────────────┘
         │
┌────────▼────────┐
│  Anthropic API  │
│  (Claude 3.5)   │
└─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- API keys: Anthropic, Pinecone (or use local Chroma)

### 1. Clone & Configure

```bash
git clone https://github.com/your-org/ai-law-compliance.git
cd ai-law-compliance
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed with sample laws
python scripts/seed_laws.py

# Start the API
uvicorn app.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App available at: http://localhost:3000

### 4. Run the Ingestion Pipeline (optional)

```bash
cd backend
python scripts/ingest_laws.py --state all --filter-ai
```

---

## 🗂️ Project Structure

```
ai-law-compliance/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/                 # Route handlers
│   │   │   ├── laws.py
│   │   │   ├── compliance.py
│   │   │   ├── search.py
│   │   │   └── ingest.py
│   │   ├── core/
│   │   │   ├── config.py        # Settings & env vars
│   │   │   └── security.py      # API key auth
│   │   ├── db/
│   │   │   ├── database.py      # SQLAlchemy setup
│   │   │   └── vector_store.py  # Pinecone/Chroma client
│   │   ├── models/
│   │   │   └── law.py           # SQLAlchemy ORM models
│   │   ├── schemas/
│   │   │   └── law.py           # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ai_filter.py     # AI relevance classifier
│   │   │   ├── compliance.py    # Compliance analysis
│   │   │   ├── embeddings.py    # Text embedding service
│   │   │   └── llm.py           # Claude API wrapper
│   │   └── utils/
│   │       └── helpers.py
│   ├── alembic/                 # DB migrations
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js app router
│   │   ├── components/          # UI components
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # React hooks
│   │   ├── lib/                 # API client, utils
│   │   └── types/               # TypeScript types
│   ├── package.json
│   └── .env.local.example
├── scripts/
│   ├── seed_laws.py             # Seed DB with sample data
│   └── ingest_laws.py          # Law ingestion pipeline
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔧 Environment Variables

See `.env.example` for all required variables:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `ANTHROPIC_API_KEY` | Claude API key |
| `PINECONE_API_KEY` | Pinecone key (or leave blank for local Chroma) |
| `PINECONE_INDEX` | Pinecone index name |
| `USE_LOCAL_VECTOR_DB` | Set to `true` to use ChromaDB instead |
| `SECRET_KEY` | JWT secret for API auth |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## 🐳 Docker (Full Stack)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/laws` | List all AI laws with filters |
| GET | `/api/laws/{id}` | Get law details |
| POST | `/api/compliance/analyze` | Analyze compliance for your company |
| POST | `/api/search` | Semantic search across laws |
| GET | `/api/laws/state/{state}` | Laws by state |
| POST | `/api/ingest` | Trigger law ingestion (admin) |

---

## 🗺️ Roadmap

- [ ] Email alerts for new/updated laws
- [ ] PDF compliance report export
- [ ] Federal law tracking (FTC, NIST AI RMF)
- [ ] EU AI Act comparison
- [ ] Slack/Teams integration

---

## 📄 License

MIT

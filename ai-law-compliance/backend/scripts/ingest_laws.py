#!/usr/bin/env python3
"""
Law ingestion pipeline.
In a real deployment this would scrape LegiScan, Legiscan API, or state legislature sites.
For MVP it accepts a JSON file of laws and processes them through the AI filter.

Usage:
  python scripts/ingest_laws.py --file laws.json
  python scripts/ingest_laws.py --state CA --filter-ai
"""
import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.law import Law
from app.db.database import Base
from app.db.vector_store import vector_store
from app.services.ai_filter import is_ai_relevant
from app.services.embeddings import embed_law
from app.services.compliance import generate_plain_english_summary

SYNC_URL = settings.DATABASE_URL.replace("+asyncpg", "")
engine = create_engine(SYNC_URL)


def ingest_from_file(filepath: str, run_ai_filter: bool = True, generate_summaries: bool = True):
    with open(filepath) as f:
        laws_data = json.load(f)

    print(f"📥 Processing {len(laws_data)} laws from {filepath}...")
    vector_store.connect()

    accepted = rejected = errors = 0

    with Session(engine) as session:
        for item in laws_data:
            title = item.get("title", "")
            summary = item.get("summary", "")
            full_text = item.get("full_text", "")

            # AI relevance filter
            if run_ai_filter:
                relevant, method = is_ai_relevant(title, summary, full_text)
                if not relevant:
                    print(f"  ⛔ Rejected [{method}]: {title[:60]}")
                    rejected += 1
                    continue

            try:
                law_id = item.get("id") or f"{item.get('state','XX').lower()}-{title[:20].lower().replace(' ','-')}"

                plain_summary = None
                if generate_summaries and full_text:
                    plain_summary = generate_plain_english_summary(title, full_text)

                existing = session.get(Law, law_id)
                if existing:
                    for k, v in item.items():
                        if hasattr(existing, k):
                            setattr(existing, k, v)
                    if plain_summary:
                        existing.plain_english_summary = plain_summary
                    law = existing
                else:
                    law = Law(
                        id=law_id,
                        is_ai_relevant=True,
                        plain_english_summary=plain_summary,
                        **{k: v for k, v in item.items() if k != "id" and hasattr(Law, k)},
                    )
                    session.add(law)

                session.flush()

                # Vector index
                embedding = embed_law(title, summary, full_text)
                vector_store.upsert(
                    doc_id=law_id,
                    embedding=embedding,
                    metadata={"state": item.get("state",""), "status": item.get("status","pending"), "risk_level": item.get("risk_level","medium"), "title": title[:200]},
                )
                law.vector_indexed = True
                accepted += 1
                print(f"  ✅ Ingested: {title[:60]}")

            except Exception as e:
                print(f"  ❌ Error: {title[:60]} — {e}")
                errors += 1

        session.commit()

    print(f"\n📊 Results: {accepted} accepted, {rejected} rejected (not AI-specific), {errors} errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest AI laws into the compliance database")
    parser.add_argument("--file", required=True, help="Path to JSON file containing laws array")
    parser.add_argument("--no-filter", action="store_true", help="Skip AI relevance filter")
    parser.add_argument("--no-summaries", action="store_true", help="Skip LLM summary generation")
    args = parser.parse_args()

    ingest_from_file(
        filepath=args.file,
        run_ai_filter=not args.no_filter,
        generate_summaries=not args.no_summaries,
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.vector_store import vector_store
from app.api import laws, compliance, search, ingest
import structlog

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Connecting to vector store...")
    vector_store.connect()
    logger.info("Vector store ready", type="local" if settings.USE_LOCAL_VECTOR_DB else "pinecone")
    yield
    # Shutdown
    logger.info("Shutting down")


app = FastAPI(
    title="AI Law Compliance Assistant",
    description="Track and analyze AI-specific legislation across U.S. states",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(laws.router)
app.include_router(compliance.router)
app.include_router(search.router)
app.include_router(ingest.router)


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

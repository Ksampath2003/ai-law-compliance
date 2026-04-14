"""
Vector store abstraction — supports ChromaDB (local) or Pinecone (cloud).
Set USE_LOCAL_VECTOR_DB=true in .env to use ChromaDB without any API keys.
"""
import uuid
from typing import List, Dict, Any, Optional
from app.core.config import settings


class VectorStore:
    def __init__(self):
        self._client = None
        self._collection = None

    def _init_chroma(self):
        import chromadb
        self._client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self._collection = self._client.get_or_create_collection(
            name="ai_laws",
            metadata={"hnsw:space": "cosine"},
        )

    def _init_pinecone(self):
        from pinecone import Pinecone
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self._client = pc.Index(settings.PINECONE_INDEX)

    def connect(self):
        if settings.USE_LOCAL_VECTOR_DB:
            self._init_chroma()
        else:
            self._init_pinecone()

    def upsert(self, doc_id: str, embedding: List[float], metadata: Dict[str, Any]):
        if settings.USE_LOCAL_VECTOR_DB:
            self._collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                metadatas=[metadata],
            )
        else:
            self._client.upsert(vectors=[(doc_id, embedding, metadata)])

    def query(self, embedding: List[float], top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        if settings.USE_LOCAL_VECTOR_DB:
            where = filters if filters else None
            results = self._collection.query(
                query_embeddings=[embedding],
                n_results=top_k,
                where=where,
                include=["metadatas", "distances"],
            )
            return [
                {"id": id_, "metadata": meta, "score": 1 - dist}
                for id_, meta, dist in zip(
                    results["ids"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                )
            ]
        else:
            resp = self._client.query(vector=embedding, top_k=top_k, include_metadata=True, filter=filters)
            return [{"id": m.id, "metadata": m.metadata, "score": m.score} for m in resp.matches]

    def delete(self, doc_id: str):
        if settings.USE_LOCAL_VECTOR_DB:
            self._collection.delete(ids=[doc_id])
        else:
            self._client.delete(ids=[doc_id])


# Singleton
vector_store = VectorStore()

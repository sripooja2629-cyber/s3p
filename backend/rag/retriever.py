import os
import json
import re
from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en")
COLLECTION_NAME = "ncert_content"


class NCERTRetriever:
    def __init__(self):
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
        print("🔄 Initializing RAG pipeline...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        os.makedirs(CHROMA_DB_PATH, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"✅ ChromaDB ready. Documents: {self.collection.count()}")
        self._initialized = True

    def embed_text(self, text: str) -> List[float]:
        if not self._initialized:
            self.initialize()
        query_text = f"Represent this sentence for searching relevant passages: {text}"
        return self.embedding_model.encode(query_text, normalize_embeddings=True).tolist()

    def ingest_batch(self, documents: List[Dict]) -> int:
        if not self._initialized:
            self.initialize()
        if not documents:
            return 0
        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        print(f"🔄 Encoding {len(texts)} documents...")
        embeddings = self.embedding_model.encode(
            texts, normalize_embeddings=True, batch_size=32, show_progress_bar=True
        ).tolist()
        self.collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        print(f"✅ Ingested {len(documents)} documents into ChromaDB")
        return len(documents)

    def retrieve(self, query: str, n_results: int = 3, subject_filter: Optional[str] = None) -> str:
        if not self._initialized:
            self.initialize()
        if self.collection.count() == 0:
            return "No NCERT content loaded yet. Please run the ingestion script."
        query_embedding = self.embed_text(query)
        where_filter = None
        if subject_filter and subject_filter != "general":
            where_filter = {"subject": {"$eq": subject_filter}}
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, self.collection.count()),
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            if not results["documents"][0]:
                return "Relevant NCERT content not found for this topic."
            context_parts = []
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                context_parts.append(
                    f"[NCERT Class {meta.get('class','')} {meta.get('subject','')} - {meta.get('chapter','')}]\n{doc}"
                )
            return "\n\n".join(context_parts)
        except Exception as e:
            print(f"❌ Retrieval error: {e}")
            return "Could not retrieve relevant NCERT content."

    def get_stats(self) -> Dict:
        if not self._initialized:
            self.initialize()
        return {
            "total_documents": self.collection.count(),
            "collection_name": COLLECTION_NAME,
            "embedding_model": EMBEDDING_MODEL,
            "db_path": CHROMA_DB_PATH
        }


_retriever_instance = None

def get_retriever() -> NCERTRetriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = NCERTRetriever()
        _retriever_instance.initialize()
    return _retriever_instance

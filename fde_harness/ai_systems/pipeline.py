"""Enterprise RAG pipeline, messy data cleaning, and structured extraction for Pillar 2."""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    chunk_id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    relevance_score: float = 0.0


class ExtractionSchema(BaseModel):
    intent: str
    entities: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    actionable_items: List[str] = Field(default_factory=list)


class EnterpriseRAGPipeline:
    """Production-grade RAG pipeline capable of handling messy, non-standard enterprise text."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.knowledge_base: List[DocumentChunk] = []

    def clean_raw_enterprise_text(self, text: str) -> str:
        """Strips excessive whitespace, OCR artifacts, and boilerplate headers/footers."""
        # Replace multiple spaces/newlines
        cleaned = re.sub(r"\r\n|\r", "\n", text)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        # Remove common disclaimer headers/footers if detected
        cleaned = re.sub(r"(?i)confidentiality notice:.*?(?=\n\n|$)", "", cleaned)
        return cleaned.strip()

    def ingest_document(self, doc_id: str, raw_text: str, metadata: Optional[Dict[str, Any]] = None) -> List[DocumentChunk]:
        """Cleans, chunks, and stores an enterprise document."""
        cleaned = self.clean_raw_enterprise_text(raw_text)
        metadata = metadata or {}
        chunks: List[DocumentChunk] = []

        start = 0
        idx = 0
        while start < len(cleaned):
            end = start + self.chunk_size
            chunk_content = cleaned[start:end]
            chunk = DocumentChunk(
                chunk_id=f"{doc_id}_{idx}",
                content=chunk_content.strip(),
                metadata={"source_doc": doc_id, "offset": start, **metadata},
            )
            chunks.append(chunk)
            self.knowledge_base.append(chunk)
            start += max(1, self.chunk_size - self.chunk_overlap)
            idx += 1

        return chunks

    def retrieve(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        """Simple, deterministic keyword-overlap ranker for retrieval without external vector API dependency."""
        query_words = set(re.findall(r"\w+", query.lower()))
        if not query_words:
            return self.knowledge_base[:top_k]

        scored_chunks = []
        for chunk in self.knowledge_base:
            chunk_words = set(re.findall(r"\w+", chunk.content.lower()))
            overlap = len(query_words.intersection(chunk_words))
            score = overlap / (len(query_words) + 1e-5)
            scored = DocumentChunk(
                chunk_id=chunk.chunk_id,
                content=chunk.content,
                metadata=chunk.metadata,
                relevance_score=round(score, 3),
            )
            scored_chunks.append(scored)

        scored_chunks.sort(key=lambda c: c.relevance_score, reverse=True)
        return scored_chunks[:top_k]

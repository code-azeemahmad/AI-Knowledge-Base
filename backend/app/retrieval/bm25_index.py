# backend\app\retrieval\bm25_index.py
from dataclasses import dataclass

from app.schemas.search import SearchResult
from app.tokenizers.base import Tokenizer
# pyrefly: ignore [missing-import]
from rank_bm25 import BM25Okapi


@dataclass
class IndexedChunk:
    id: str
    text: str
    payload: dict

class BM25Index:

    def __init__(
        self,
        tokenizer: Tokenizer,
    ):
        self.tokenizer = tokenizer

        self.documents: list[IndexedChunk] = []

        self.corpus: list[list[str]] = []

        self.bm25: BM25Okapi | None = None

    def add_documents(
        self,
        chunks: list[IndexedChunk],
    ) -> None:
        """
        Add document chunks to the BM25 index and rebuild it.
        """
        self.documents.extend(chunks)
        self.rebuild()


    def rebuild(self) -> None:

        self.corpus = [
            self.tokenizer.tokenize(doc.text)
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(self.corpus)


    def remove_document(
        self,
        document_id: str,
    ) -> None:

        self.documents = [
            doc
            for doc in self.documents
            if doc.payload["document_id"] != document_id
        ]

        self.rebuild()


    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[SearchResult]:
        """Perform BM25 keyword search over indexed documents."""
        # 1. Guard check: return empty list if BM25 index is not initialized
        if self.bm25 is None:
            return []

        # 2. Tokenize the incoming search query
        tokens = self.tokenizer.tokenize(query)

        # 3. Calculate BM25 scores for all documents
        scores = self.bm25.get_scores(tokens)

        # 4. Pair documents with scores and sort in descending order
        ranked = sorted(
            zip(self.documents, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        # 5. Convert top results into SearchResult objects
        results = [
            SearchResult(
                id=document.id,
                score=float(score),
                payload=document.payload,
            )
            for document, score in ranked[:limit]
            if score > 0
        ][:limit]

        return results
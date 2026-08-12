# AI-Knowledge-Base\backend\app\retrieval\sparse.py
from app.retrieval.base import BaseRetriever
from app.retrieval.bm25_index import BM25Index
from app.schemas.search import SearchResult


class SparseRetriever(BaseRetriever):
    """
    Keyword-based retriever backed by a BM25 index.
    """

    def __init__(
        self,
        bm25_index: BM25Index,
    ):
        self.bm25_index = bm25_index

    async def retrieve(
        self,
        question: str,
        limit: int | None = None,
        document_id: str | None = None,
    ) -> list[SearchResult]:

        search_limit = limit or 20

        results = self.bm25_index.search(
            query=question,
            limit=search_limit,
        )

        if document_id is None:
            return results

        return [
            result
            for result in results
            if result.payload.get("document_id") == document_id
        ]
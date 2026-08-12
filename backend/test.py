# backend/test_pipeline.py
import asyncio

from app.core.dependencies import (
    get_dense_retriever,
    get_hybrid_retriever,
    get_sparse_retriever,
)
from app.rerankers.cross_encoder_reranker import CrossEncoderReranker
from app.schemas.search import SearchResult
from app.services.rag_service import RAGService
from sentence_transformers import CrossEncoder

TEST_QUERIES = [
    "What is SKU-123?",
    "How do I use FastAPI Depends?",
    "When should I use asyncio.gather?",
    "What is HTTP 404?",
    "What are the specs of GPT-4.1?",
]


def extract_text(payload: dict) -> str:
    """Safely extracts text content from document payload regardless of key variations."""
    if not payload:
        return ""
    return (
        payload.get("text")
        or payload.get("content")
        or payload.get("page_content")
        or str(payload)
    )


def print_results(title: str, results: list[SearchResult], snippet_len: int = 80):
    """Helper to display formatted search result lists safely."""
    print(f"\n--- {title} (Count: {len(results)}) ---")
    if not results:
        print("  [No results returned]")
        return
    for rank, r in enumerate(results, start=1):
        text_content = extract_text(r.payload)
        text_snippet = text_content.replace("\n", " ")[:snippet_len]
        print(f"  [{rank}] Score: {r.score:.4f} | Text: {text_snippet}...")


async def run_pipeline_verification():
    print("=" * 80)
    print("      RAG PIPELINE COMPONENT & HYBRID RETRIEVAL VERIFICATION")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 0. INITIALIZE RETRIEVERS & RERANKER DIRECTLY
    # -------------------------------------------------------------------------
    dense = get_dense_retriever()
    sparse = get_sparse_retriever()
    hybrid = get_hybrid_retriever()

    # Load CrossEncoder directly for standalone execution (replace with your model name if different)
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    reranker = CrossEncoderReranker(model=model)

    # =========================================================================
    # TEST 1 & 2: DENSE VS SPARSE BASELINE COMPARISON
    # =========================================================================
    print("\n" + "=" * 50)
    print("TEST 1 & 2: DENSE VS SPARSE BASELINE COMPARISON")
    print("=" * 50)
    sample_q = "FastAPI Depends"

    dense_res = await dense.retrieve(sample_q, limit=5)
    sparse_res = await sparse.retrieve(sample_q, limit=5)

    print_results("Dense Results Baseline", dense_res)
    print_results("Sparse BM25 Results Baseline", sparse_res)

    # =========================================================================
    # TEST 3 & 4: EXACT KEYWORD RETRIEVAL MATRIX
    # =========================================================================
    print("\n" + "=" * 50)
    print("TEST 3 & 4: EXACT KEYWORD RETRIEVAL MATRIX")
    print("=" * 50)

    for query in TEST_QUERIES:
        print("\n" + "#" * 70)
        print(f"QUERY: '{query}'")
        print("#" * 70)

        d_res = await dense.retrieve(query, limit=5)
        s_res = await sparse.retrieve(query, limit=5)
        h_res = await hybrid.retrieve(query, limit=5)

        print_results("DENSE RETRIEVER", d_res)
        print_results("SPARSE (BM25) RETRIEVER", s_res)
        print_results("HYBRID RETRIEVER (RRF FUSED)", h_res)

        target_terms = ["sku-123", "404", "gpt-4.1", "asyncio.gather", "depends"]
        has_exact_in_dense = any(
            q_term in extract_text(r.payload).lower()
            for r in d_res
            for q_term in target_terms
        )
        has_exact_in_sparse = any(
            q_term in extract_text(r.payload).lower()
            for r in s_res
            for q_term in target_terms
        )

        print("\n[VERIFICATION OBSERVATION]")
        print(f" -> Dense retrieved exact token match : {has_exact_in_dense}")
        print(f" -> Sparse retrieved exact token match: {has_exact_in_sparse}")

    # =========================================================================
    # TEST 5: RRF FUSION & CROSS-ENCODER RERANKING
    # =========================================================================
    print("\n" + "=" * 50)
    print("TEST 5: RRF FUSION & CROSS-ENCODER RERANKING")
    print("=" * 50)

    rerank_query = "What is SKU-123?"
    print(f"Testing pipeline ordering for: '{rerank_query}'")

    hybrid_candidates = await hybrid.retrieve(rerank_query, limit=10)
    print_results("Pre-Rerank (Hybrid Candidate Pool)", hybrid_candidates)

    reranked_res = await reranker.rerank(
        rerank_query, hybrid_candidates, top_k=3
    )

    print_results("Post-Rerank (Cross-Encoder Top-3)", reranked_res)

    if reranked_res:
        top_text = extract_text(reranked_res[0].payload)
        if "SKU-123" in top_text:
            print(
                "\nSUCCESS: Cross-Encoder promoted 'SKU-123' chunk to Rank 1!"
            )
        else:
            print(
                "\nWARNING: Rank 1 chunk does not contain 'SKU-123'. Check reranker scores."
            )

    # =========================================================================
    # TEST 6: FULL END-TO-END RAG SYNTHESIS
    # =========================================================================
    print("\n" + "=" * 50)
    print("TEST 6: END-TO-END RAG GENERATION WITH HYBRID + RERANK")
    print("=" * 50)

    rag_service = RAGService(retriever=hybrid, reranker=reranker)

    for rag_q in [
        "What hardware model corresponds to SKU-123?",
        "How should I handle HTTP 404 in FastAPI?",
    ]:
        print(f"\n[RAG Question]: {rag_q}")

        response = await rag_service.answer_question(
            conversation_id="test_session_1",
            question=rag_q,
        )

        print("\n[LLM Generated Answer]:")
        print("-" * 60)
        print(response.answer if hasattr(response, "answer") else response)
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(run_pipeline_verification())
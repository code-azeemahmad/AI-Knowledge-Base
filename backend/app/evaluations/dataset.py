# backend\app\evaluations\dataset.py
"""
Evaluation dataset for the RAG pipeline.

relevant_chunk_ids are matched against result.payload["chunk_index"]
and result.payload["filename"] so the dataset stays stable even when
Qdrant point UUIDs change after re-indexing.

EvaluationSample.relevant_chunk_ids stores values in the format:
    "<filename>:<chunk_index>"

The RetrievalEvaluator normalises retrieved SearchResult IDs to the
same format before comparison.
"""
from app.evaluations.models import EvaluationSample


EVALUATION_DATASET: list[EvaluationSample] = [
    EvaluationSample(
        question="What is Retrieval-Augmented Generation?",
        relevant_chunk_ids=[
            "rag_sample_5pages.pdf:0",
            "rag_sample_5pages.pdf:1",
        ],
        expected_answer=(
            "Retrieval-Augmented Generation (RAG) is a technique that "
            "combines information retrieval with large language model "
            "generation to produce accurate, grounded responses."
        ),
    ),
    EvaluationSample(
        question="What are the core components of a RAG pipeline?",
        relevant_chunk_ids=[
            "rag_sample_5pages.pdf:1",
            "rag_sample_5pages.pdf:2",
        ],
        expected_answer=(
            "The core components include ingestion, chunking, embedding "
            "generation, vector storage, retrieval, and response generation."
        ),
    ),
    EvaluationSample(
        question="How does vector search work in RAG?",
        relevant_chunk_ids=[
            "rag_sample_5pages.pdf:2",
            "rag_sample_5pages.pdf:3",
        ],
        expected_answer=(
            "Vector search converts text into high-dimensional embeddings "
            "and finds nearest neighbours using cosine or dot-product similarity."
        ),
    ),
]

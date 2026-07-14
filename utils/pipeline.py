"""
=========================================================
Enterprise AI Knowledge Assistant
RAG Pipeline
=========================================================

This file contains the complete Retrieval-Augmented
Generation (RAG) workflow.

Pipeline:
PDF(s)
    ↓
Load PDF
    ↓
Split into Chunks
    ↓
Create Embeddings
    ↓
Build FAISS Vector Store
    ↓
Save Vector Store
    ↓
User Question
    ↓
Retrieve Relevant Chunks
    ↓
Generate Answer using Gemini
"""

# =========================================================
# IMPORTS
# =========================================================

from .pdf_loader import load_pdf
from .text_splitter import split_pages

from .embedding_model import (
    create_embeddings,
    embed_query
)

from .vector_database import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    search_vector_store
)

from .llm import generate_answer


# =========================================================
# BUILD KNOWLEDGE BASE
# =========================================================

def build_knowledge_base(uploaded_files):
    """
    Process uploaded PDF files and create
    the vector database.

    Parameters
    ----------
    uploaded_files : list
        List of uploaded PDF files.

    Returns
    -------
    vector_store
        FAISS Index

    documents
        List containing all document chunks
        with metadata.
    """

    all_documents = []

    # Process each uploaded PDF
    for file in uploaded_files:

        # Extract pages
        pages = load_pdf(file)

        # Split into chunks
        documents = split_pages(
            pages,
            file.name
        )

        # Store all chunks
        all_documents.extend(documents)

    # Create embeddings
    embeddings = create_embeddings(all_documents)

    # Create FAISS vector store
    vector_store = create_vector_store(
        embeddings
    )

    # Save index + metadata
    save_vector_store(
        vector_store,
        all_documents
    )

    return vector_store, all_documents


# =========================================================
# LOAD EXISTING KNOWLEDGE BASE
# =========================================================

def load_knowledge_base():
    """
    Load the previously saved
    FAISS vector database.

    Returns
    -------
    vector_store

    documents
    """

    vector_store, documents = load_vector_store()

    return vector_store, documents


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    question,
    vector_store,
    documents,
    top_k=3
):
    """
    Retrieve the most relevant
    document chunks.

    Parameters
    ----------
    question : str

    vector_store

    documents

    top_k : int

    Returns
    -------
    results
    """

    query_embedding = embed_query(question)

    results = search_vector_store(
        vector_store,
        query_embedding,
        documents,
        top_k
    )

    return results


# =========================================================
# BUILD CONTEXT
# =========================================================

def build_context(results):
    """
    Convert retrieved documents into
    one context string.

    Parameters
    ----------
    results

    Returns
    -------
    context : str
    """

    context = "\n\n".join(

        doc["text"]

        for doc in results

    )

    return context


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question(
    question,
    vector_store,
    documents
):
    """
    Complete RAG pipeline.

    Steps

    User Question
        ↓
    Embed Question
        ↓
    Semantic Search
        ↓
    Build Context
        ↓
    Gemini
        ↓
    Final Answer
    """

    # Retrieve relevant chunks
    results = retrieve_documents(
        question,
        vector_store,
        documents
    )

    # Convert chunks into context
    context = build_context(results)

    # Generate answer
    answer = generate_answer(
        context,
        question
    )

    return answer, results


# =========================================================
# GET KNOWLEDGE BASE STATS
# =========================================================

def get_statistics(
    vector_store,
    documents
):
    """
    Returns useful statistics.

    Returns
    -------
    dict
    """

    stats = {

        "vectors": vector_store.ntotal,

        "chunks": len(documents),

        "documents": len(
            set(
                doc["source"]
                for doc in documents
            )
        )

    }

    return stats
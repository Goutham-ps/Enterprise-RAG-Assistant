import streamlit as st
from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_embedding_model():
    """
    Load and cache the embedding model.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(documents):
    """
    Create embeddings from document text.
    """

    model = load_embedding_model()

    texts = [doc["text"] for doc in documents]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings


def embed_query(query):
    """
    Create an embedding for the user's question.
    """

    model = load_embedding_model()

    return model.encode(
        [query],
        convert_to_numpy=True
    )
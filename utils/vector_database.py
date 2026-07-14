import os
import pickle
import faiss
import numpy as np

VECTOR_DIR = "vectorstore"

INDEX_FILE = os.path.join(VECTOR_DIR, "faiss.index")
DOCUMENTS_FILE = os.path.join(VECTOR_DIR, "documents.pkl")


def create_vector_store(embeddings):
    """
    Create a FAISS vector index.
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index


def save_vector_store(index, documents):
    """
    Save FAISS index and document metadata.
    """

    os.makedirs(VECTOR_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_FILE)

    with open(DOCUMENTS_FILE, "wb") as f:
        pickle.dump(documents, f)


def load_vector_store():
    """
    Load FAISS index and documents.
    """

    if not os.path.exists(INDEX_FILE):
        return None, None

    index = faiss.read_index(INDEX_FILE)

    with open(DOCUMENTS_FILE, "rb") as f:
        documents = pickle.load(f)

    return index, documents


def search_vector_store(index, query_embedding, documents, top_k=3):
    """
    Search similar documents.
    """

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:

        if idx != -1:

            results.append(documents[idx])

    return results
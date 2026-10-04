import numpy as np
import faiss

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def split_text(text, chunk_size=500):
    """
    Split large text into smaller chunks.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


def create_vector_database(chunks):
    """
    Convert chunks into embeddings
    and store them in FAISS.
    """

    embeddings = embedding_model.encode(
        chunks
    )

    embeddings = np.array(
        embeddings
    ).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index


def search_documents(
    query,
    chunks,
    index,
    top_k=3
):
    """
    Find the most relevant chunks
    for a user question.
    """

    query_embedding = embedding_model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for index_number in indices[0]:
        if index_number < len(chunks):
            results.append(
                chunks[index_number]
            )

    return results
"""
This module embeds processed documents using Gemini embeddings
and stores them in a FAISS vector database for fast semantic retrieval.
"""

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def store_in_faiss(docs, index_name: str = "faiss_budget_index"):
    """
    Creates embeddings for the given documents (in safe batches of 100)
    and stores them in a FAISS index for retrieval.

    Args:
        docs (List[Document]): List of processed LangChain Document objects.
        index_name (str): Directory name to save the FAISS index.

    Returns:
        FAISS: Vector store object containing all embeddings.
    """

    embedding_model_name = "models/text-embedding-004"
    print(f" Creating embeddings using: {embedding_model_name}")

    # Initialize Gemini Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model_name)

    # Gemini API allows only 100 embeddings per batch
    batch_size = 100
    all_stores = []

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        print(f" Processing batch {i // batch_size + 1} of {(len(docs) // batch_size) + 1} "
              f"({len(batch)} docs)")
        batch_store = FAISS.from_documents(batch, embeddings)
        all_stores.append(batch_store)

    # Merge all batches into one FAISS index
    vectorstore = all_stores[0]
    for extra_store in all_stores[1:]:
        vectorstore.merge_from(extra_store)

    print(f" FAISS index created with {len(docs)} documents.")
    vectorstore.save_local(index_name)
    print(f" FAISS index saved locally as '{index_name}/'")

    return vectorstore


def load_faiss(index_name: str = "faiss_budget_index"):
    """
    Loads an existing FAISS vector store from the local directory.

    Args:
        index_name (str): Directory name where FAISS index is stored.

    Returns:
        FAISS: Loaded vector store ready for retrieval.
    """

    embedding_model_name = "models/text-embedding-004"
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model_name)

    vectorstore = FAISS.load_local(
        index_name,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f" Loaded FAISS index from '{index_name}/'")
    return vectorstore


# Example usage (run directly)
if __name__ == "__main__":
    from splitter import split_documents
    from loader import load_budget_pdf_auto

    # Ensure API key is available
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    # Load two budget PDFs
    pdfs = [
        ("budget_speech_24_25.pdf", "2024-25"),
        ("budget_speech_25_26.pdf", "2025-26")
    ]

    all_docs = []
    for path, label in pdfs:
        docs = load_budget_pdf_auto(path, label)
        all_docs.extend(docs)

    # Split for embeddings
    docs_ready = split_documents(all_docs)

    # Store into FAISS
    vectorstore = store_in_faiss(docs_ready, index_name="budget_faiss_index")

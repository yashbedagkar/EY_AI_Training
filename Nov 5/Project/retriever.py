"""
 MultiQuery Retriever and Context Builder for RAG Chatbot
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.retrievers.multi_query import MultiQueryRetriever

# Load environment variables
load_dotenv()

def load_retriever(
    index_name: str = "budget_faiss_index",
    k: int = 6,
    model_name: str = "gemini-2.5-flash"
):
    """Loads FAISS index and builds MultiQueryRetriever."""
    # Embedding model
    embedding_model_name = "models/text-embedding-004"
    embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model_name)

    # Load FAISS index
    vectorstore = FAISS.load_local(
        index_name,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # LLM for query expansion
    llm = GoogleGenerativeAI(model=model_name, temperature=0)

    # Build MultiQuery retriever
    retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(search_kwargs={"k": k}),
        llm=llm
    )

    print(f" MultiQueryRetriever is ready (k={k}, model={model_name})")
    return retriever


def build_context(docs: List[Document]) -> str:
    """Combine top retrieved documents into a single context string."""
    context_parts = []
    for d in docs:
        year = d.metadata.get("year", "unknown-year")
        page = d.metadata.get("page", "?")
        dtype = d.metadata.get("type", "text")
        text = d.page_content.strip().replace("\n", " ")
        if len(text) > 1000:
            text = text[:1000] + " ..."
        context_parts.append(f"[{year} | page {page} | {dtype}] {text}")
    return "\n\n".join(context_parts)


# Example usage
if __name__ == "__main__":
    retriever = load_retriever(index_name="budget_faiss_index", k=6)
    query = "What are the key budget allocations for the education sector in 2025-26?"
    docs = retriever.invoke(query)
    print(f"Retrieved {len(docs)} relevant documents.")
    print(build_context(docs)[:500] + "...")

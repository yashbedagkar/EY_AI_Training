"""
Splits textual and tabular PDF content into embedding-friendly chunks,
combines both budget PDFs, and saves the result in JSON format.
"""

import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(docs, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits a list of LangChain Document objects into smaller chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    processed_docs = []

    for d in docs:
        doc_type = d.metadata.get("type", "text").lower()

        if "text" in doc_type:
            chunks = splitter.split_text(d.page_content)
            for i, chunk in enumerate(chunks):
                md = dict(d.metadata)
                md["chunk_index"] = i
                processed_docs.append(Document(page_content=chunk, metadata=md))

        elif "table" in doc_type:
            if len(d.page_content) > chunk_size:
                chunks = splitter.split_text(d.page_content)
                for i, chunk in enumerate(chunks):
                    md = dict(d.metadata)
                    md["chunk_index"] = i
                    processed_docs.append(Document(page_content=chunk, metadata=md))
            else:
                processed_docs.append(d)
        else:
            processed_docs.append(d)

    print(f"Split completed: {len(processed_docs)} final chunks generated.")
    return processed_docs


# --- JSON Conversion Helpers ---

def docs_to_json(docs, output_path):
    """Save Document list to JSON."""
    data = [
        {"page_content": d.page_content, "metadata": d.metadata}
        for d in docs
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f" Saved {len(docs)} documents to {output_path}")


def json_to_docs(input_path):
    """Load JSON into Document list."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    docs = [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in data]
    print(f" Loaded {len(docs)} documents from {input_path}")
    return docs


# --- Main Execution ---
if __name__ == "__main__":
    from loader import load_budget_pdf_auto

    pdf_path_24_25 = "budget_speech_24_25.pdf"
    pdf_path_25_26 = "budget_speech_25_26.pdf"

    all_docs = []

    for path, label in [(pdf_path_24_25, "2024-25"), (pdf_path_25_26, "2025-26")]:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
        docs = load_budget_pdf_auto(path, label)
        all_docs.extend(docs)

    docs_ready = split_documents(all_docs)
    print(f" Total chunks after splitting: {len(docs_ready)}")

    # Save as JSON instead of pickle
    docs_to_json(docs_ready, "split_docs.json")

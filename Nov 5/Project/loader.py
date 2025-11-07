
"""
PDF Loader using PyMuPDF + pdfplumber
Extracts both textual and tabular data 
"""

import fitz  # PyMuPDF
import pdfplumber
from langchain_core.documents import Document
import os


def extract_text_with_fitz(pdf_path: str, year_label: str):
    """Extract text content from PDF using PyMuPDF (fast)."""
    docs = []
    with fitz.open(pdf_path) as pdf:
        for i, page in enumerate(pdf):
            text = page.get_text("text")
            if text.strip():
                docs.append(
                    Document(
                        page_content=text.strip(),
                        metadata={"year": year_label, "page": i + 1, "type": "text"},
                    )
                )
    print(f" Extracted {len(docs)} text docs from {pdf_path}")
    return docs


def extract_tables_with_pdfplumber(pdf_path: str, year_label: str):
    """Extract tabular data using pdfplumber """
    docs = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for t_idx, table in enumerate(tables):
                if not table or len(table) < 2:
                    continue
                headers = table[0]
                rows = table[1:]
                csv_text = "\n".join([",".join([str(cell) if cell is not None else "" for cell in row])for row in [headers] + rows])
                docs.append(
                    Document(
                        page_content=csv_text,
                        metadata={
                            "year": year_label,
                            "page": i + 1,
                            "type": "table",
                            "table_index": t_idx,
                        },
                    )
                )
    print(f" Extracted {len(docs)} tables from {pdf_path}")
    return docs


def load_budget_pdf_auto(pdf_path: str, year_label: str):
    """Combines text + table extraction into one loader."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f" PDF not found: {pdf_path}")

    print(f"\n Loading {pdf_path} for year {year_label}...")
    text_docs = extract_text_with_fitz(pdf_path, year_label)
    table_docs = extract_tables_with_pdfplumber(pdf_path, year_label)
    all_docs = text_docs + table_docs
    print(f" Loaded {len(all_docs)} total docs from {pdf_path}")
    return all_docs


def preview_docs(docs, n=5):
    """Preview sample documents."""
    print(f"\n Previewing {min(n, len(docs))} documents:\n")
    for d in docs[:n]:
        print("—" * 60)
        print("META:", d.metadata)
        print("CONTENT:", d.page_content[:250].replace("\n", " "))
    print("—" * 60)


if __name__ == "__main__":
    pdf_path_24_25 = "budget_speech_24_25.pdf"
    pdf_path_25_26 = "budget_speech_25_26.pdf"

    all_docs = []
    for path, label in [(pdf_path_24_25, "2024-25"), (pdf_path_25_26, "2025-26")]:
        all_docs += load_budget_pdf_auto(path, label)

    print(f"\n Combined total: {len(all_docs)} documents loaded.")
    preview_docs(all_docs)
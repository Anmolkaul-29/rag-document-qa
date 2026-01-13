import os
from backend.loader import load_pdf
from backend.chunker import chunk_text
from backend.vectorstore import embed_texts, save_index

def ingest_document(file_path):
    pages = load_pdf(file_path)

    texts = []
    metadatas = []

    for page in pages:
        if not page["text"]:
            continue

        chunks = chunk_text(
            page["text"],
            {"page": page["page"], "doc": os.path.basename(file_path)}
        )

        for c in chunks:
            texts.append(c["content"])
            metadatas.append({
                "doc": c["metadata"]["doc"],
                "page": c["metadata"]["page"],
                "text": c["content"]   # 👈 CRITICAL
            })

    if not texts:
        raise ValueError(
            "No readable text found in document. "
            "The document may be scanned or image-based."
        )


    embeddings = embed_texts(texts)
    save_index(embeddings, metadatas)

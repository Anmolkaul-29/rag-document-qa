from pypdf import PdfReader

def load_pdf(path):
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        # ✅ Defensive check (CRITICAL)
        if text and text.strip():
            pages.append({
                "text": text,
                "page": i + 1
            })

    return pages

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text, metadata):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)
    return [
        {"content": chunk, "metadata": metadata}
        for chunk in chunks
    ]

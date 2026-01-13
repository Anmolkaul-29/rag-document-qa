from dotenv import load_dotenv
load_dotenv()

import os
import numpy as np
from openai import OpenAI
from backend.vectorstore import load_index, embed_texts
from backend.memory import get_memory, update_memory

client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1"
)

def chat_with_docs(session_id, query):
    index, metadata = load_index()
    query_vector = embed_texts([query])

    D, I = index.search(query_vector, k=8)

    context_chunks = []
    sources = set()

    for i in I[0]:
        meta = metadata[i]
        context_chunks.append(
            f"Document: {meta['doc']} | Page: {meta.get('page', 'N/A')}\n"
            f"Content:\n{meta['text']}"
        )

        sources.add(meta["doc"])

    context = "\n".join(context_chunks)

    if not context.strip():
        return "Not found in the documents.", []

    history = get_memory(session_id)[-6:]

    prompt = f"""
You are a document-based Question Answering assistant.

Instructions:
- Use ONLY the provided context.
- Do NOT use prior knowledge.
- Do NOT infer or assume missing details.
- If the answer is not explicitly present, respond exactly with:
  "Not found in the documents."

Conversation History:
{history}

Retrieved Context:
{context}

User Question:
{query}
"""

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content.strip()

    update_memory(session_id, "user", query)
    update_memory(session_id, "assistant", answer)

    return answer, list(sources)

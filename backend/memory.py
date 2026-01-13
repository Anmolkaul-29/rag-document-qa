conversation_store = {}

def get_memory(session_id):
    return conversation_store.get(session_id, [])[-5:]

def update_memory(session_id, role, content):
    conversation_store.setdefault(session_id, []).append({
        "role": role,
        "content": content
    })

def reset_memory(session_id):
    conversation_store.pop(session_id, None)

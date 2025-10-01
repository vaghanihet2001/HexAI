import os
import json
from typing import Any, Dict, List
from sentence_transformers import SentenceTransformer
import chromadb

# ----------------- File & DB setup -----------------
MEMORY_FILE = os.path.join("data", "memory.json")

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(name="memory")

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------- Helper functions -----------------
def _ensure_memory_file():
    """Ensure memory.json exists."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({"notes": ["Welcome to HEX AI"]}, f, indent=4)


def get_embedding(text: str) -> List[float]:
    """Generate embedding vector using SentenceTransformers."""
    try:
        vector = embedding_model.encode(text)
        return vector.tolist()
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return []


def add_to_vector_db(key: str, value: str):
    """Add a memory item to ChromaDB."""
    emb = get_embedding(value)
    vector_id = f"{key}_{hash(value)}"
    collection.add(ids=[vector_id], documents=[value], embeddings=[emb])


def remove_from_vector_db(key: str):
    """Remove all vectors related to a memory key from ChromaDB."""
    # ChromaDB allows delete by IDs; collect matching IDs
    all_vectors = collection.get()
    ids_to_remove = [v["id"] for v in all_vectors["ids"] if v.startswith(f"{key}_")]
    if ids_to_remove:
        collection.delete(ids=ids_to_remove)


# ----------------- Memory JSON operations -----------------
def load_memory() -> Dict[str, Any]:
    """Load the memory.json content."""
    _ensure_memory_file()
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory: Dict[str, Any]):
    """Save the updated memory to memory.json."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def get_memory(key: str = None) -> Any:
    """Get full memory or a specific key."""
    memory = load_memory()
    if key:
        return memory.get(key)
    return memory


def add_memory(key: str, value: Any):
    """Add a new entry or append to an existing list, update vector DB."""
    memory = load_memory()
    if key not in memory:
        memory[key] = value if isinstance(value, list) else [value]
    else:
        if isinstance(memory[key], list):
            memory[key].append(value)
        else:
            memory[key] = value
    save_memory(memory)

    # Add to vector DB
    if isinstance(memory[key], list):
        add_to_vector_db(key, str(value))
    else:
        add_to_vector_db(key, str(memory[key]))


def update_memory(key: str, value: Any):
    """Update or overwrite a memory key, update vector DB."""
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

    # Remove old vectors
    remove_from_vector_db(key)

    # Add new vector(s)
    if isinstance(value, list):
        for v in value:
            add_to_vector_db(key, str(v))
    else:
        add_to_vector_db(key, str(value))


def delete_memory(key: str):
    """Delete a memory key and remove from vector DB."""
    memory = load_memory()
    if key in memory:
        del memory[key]
        save_memory(memory)

    # Remove from vector DB
    remove_from_vector_db(key)


# ----------------- Quick test -----------------
if __name__ == "__main__":
    print("📖 Current Memory:", get_memory())
    add_memory("tasks", "Finish chatbot module")
    print("✅ After Adding:", get_memory())
    update_memory("notes", ["Custom welcome message"])
    print("✏️ After Updating Notes:", get_memory())
    delete_memory("tasks")
    print("🗑️ After Deleting tasks:", get_memory())

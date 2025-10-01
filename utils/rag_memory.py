import chromadb
from utils.memory import get_memory
from typing import List
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(name="memory")

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2",device="cpu")  # small & fast

def get_embedding(text: str) -> List[float]:
    """Generate embedding vector using SentenceTransformers."""
    try:
        vector = embedding_model.encode(text)
        return vector.tolist()
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return []

# --- Add memory to vector DB ---
def add_memory_to_db(key: str, value: str):
    """
    Add a single memory fact to ChromaDB.
    """
    emb = get_embedding(value)
    # Use a unique ID for vector DB
    vector_id = f"{key}_{hash(value)}"
    collection.add(ids=[vector_id], documents=[value], embeddings=[emb])
    print(f"✅ Added memory to DB: {key} -> {value}")

# --- Index all memory.json ---
def index_memory_from_json():
    memory = get_memory()
    for key, value in memory.items():
        if isinstance(value, list):
            for v in value:
                add_memory_to_db(key, str(v))
        else:
            add_memory_to_db(key, str(value))
    print("✅ All memory indexed into ChromaDB.")

# --- Retrieve relevant memory ---
def retrieve_memory(query: str, n_results: int = 5) -> str:
    q_emb = get_embedding(query)
    results = collection.query(query_embeddings=[q_emb], n_results=n_results)
    docs = results.get("documents", [[]])[0]
    return "\n".join(docs)

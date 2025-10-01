import chromadb
from utils.rag_memory import index_memory_from_json
# index_memory_from_json()
# Open the persistent client
client = chromadb.PersistentClient(path="./memory_db")
collection = client.get_or_create_collection(name="memory")

# Get all stored records
all_vectors = collection.get()
print("IDs:", all_vectors["ids"])
print("Documents:", all_vectors["documents"])
# print("Embeddings (first vector example):", all_vectors["embeddings"][0])

# Delete all items in the collection
# collection.delete(ids=all_vectors["ids"])  # empty `where` deletes everything
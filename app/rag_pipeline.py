import os
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# -------- CONFIG -------- #
MODEL_NAME = "BAAI/bge-small-en"
TEXT_FILE = "input/clean_text.txt"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 120
# ------------------------ #

# Initialize the embedding function for Chroma (✅ consistent with assistant)
embedding_function = SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
model = SentenceTransformer(MODEL_NAME)

def chunk_text(text, chunk_size=600, overlap=120):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def build_chroma():
    if not os.path.exists(TEXT_FILE):
        raise FileNotFoundError(f"❌ Text file not found: {TEXT_FILE}")

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"[INFO] Created {len(chunks)} chunks ✅")

    client = PersistentClient(path="vectorstore")

    # ✅ Use same embedding function as assistant
    collection = client.get_or_create_collection(
        name="rag_docs_final",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

    # Clean up previous data
    try:
        collection.delete(where={})
    except:
        pass

    print("[INFO] Encoding text and adding to vector store...")
    embeddings = model.encode(chunks, show_progress_bar=True).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(ids=ids, documents=chunks, embeddings=embeddings)

    print("\n✅ Vector store successfully built and saved to: vectorstore/")
    return collection

if __name__ == "__main__":
    build_chroma()

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# === Initialize embeddings & ChromaDB ===
embedder = SentenceTransformer("BAAI/bge-small-en")
client = PersistentClient(path="vectorstore")

try:
    collection = client.get_collection("rag_docs")
except:
    collection = client.get_collection("rag_chunks")

print(f"📚 Using collection: {collection.name}")

# === Initialize LLM ===
print("🧠 Loading local LLM model (flan-t5-base)...")
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# === Query Loop ===
while True:
    query = input("\n❓ Enter your question (or type 'exit' to quit): ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting RAG Assistant.")
        break

    # 1️⃣ Retrieve top chunks
    query_emb = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_emb, n_results=5)
    docs = results.get("documents", [[]])[0]

    if not docs:
        print("⚠️ No relevant information found.")
        continue

    # 2️⃣ Combine top contexts
    context = "\n\n".join(docs)

    # 3️⃣ Generate answer using LLM
    prompt = f"Answer the question based on the context below.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    answer = generator(prompt, max_new_tokens=200, temperature=0.7)[0]["generated_text"]

    # 4️⃣ Print results
    print("\n💬 RAG Answer:\n", answer)

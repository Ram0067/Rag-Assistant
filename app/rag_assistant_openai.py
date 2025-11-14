import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from openai import OpenAI
from rag_visualizer import visualize_from_context

# ---------------------------------------------
# 1️⃣ Load environment
# ---------------------------------------------
load_dotenv()
deepseek_key = os.getenv("DEEPSEEK_API_KEY")

if not deepseek_key:
    raise ValueError("❌ Missing DEEPSEEK_API_KEY. Please set it via: setx DEEPSEEK_API_KEY 'your_key_here'")

# ---------------------------------------------
# 2️⃣ Initialize DeepSeek client
# ---------------------------------------------
client = OpenAI(api_key=deepseek_key, base_url="https://openrouter.ai/api/v1")
print("🤖 Using DeepSeek R1 API successfully authenticated ✅")

# ---------------------------------------------
# 3️⃣ Connect to Chroma vector store
# ---------------------------------------------
MODEL_NAME = "BAAI/bge-small-en"
embedding_function = SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)

chroma_client = chromadb.PersistentClient(path="vectorstore")
collection_name = "rag_docs_final"

try:
    collection = chroma_client.get_collection(collection_name, embedding_function=embedding_function)
    print(f"📚 Using existing Chroma collection: {collection_name}")
except Exception:
    collection = chroma_client.create_collection(collection_name, embedding_function=embedding_function)
    print(f"🆕 Created new Chroma collection: {collection_name}")

# ---------------------------------------------
# 4️⃣ DeepSeek-powered RAG generator
# ---------------------------------------------
def generate_answer(question, context):
    prompt = f"""
You are a Retrieval-Augmented Generation (RAG) assistant.
Use the provided context to generate an accurate and concise answer.

Context:
{context}

Question:
{question}

Answer:
"""
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in AI and RAG."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

# ---------------------------------------------
# 5️⃣ Interactive RAG chat loop with live visualization
# ---------------------------------------------
while True:
    question = input("\n❓ Ask a question (or type 'exit' to quit): ").strip()
    if question.lower() in ["exit", "quit"]:
        print("👋 Exiting RAG Assistant. Goodbye!")
        break

    results = collection.query(query_texts=[question], n_results=5)
    docs = results["documents"][0] if results["documents"] else []

    if not docs:
        print("⚠️ No relevant context found.")
        continue

    context = "\n".join(docs)

    try:
        answer = generate_answer(question, context)
        print("\n💬 RAG Answer:\n", answer)
    except Exception as e:
        print(f"\n❌ Error generating response: {e}")
        continue

    # 🧠 Auto-generate RAG visualization for current question
    try:
        visualize_from_context(f"Question: {question}\nAnswer: {answer}\nContext: {context}", query=question)
    except Exception as e:
        print(f"⚠️ Visualization skipped due to error: {e}")

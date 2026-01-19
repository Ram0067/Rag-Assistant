import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from openai import OpenAI
from dotenv import load_dotenv
import os

from rag_visualizer import extract_rag_keywords, detect_flow_pattern, generate_rag_flow_diagram

# Load environment
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Groq Client
client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/v1")

# Chroma Setup
embedding_function = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-small-en")
chroma_client = chromadb.PersistentClient(path="vectorstore")
collection = chroma_client.get_collection("rag_docs_final", embedding_function=embedding_function)

# Streamlit UI
st.title("🔍 RAG Assistant (Streamlit + DeepSeek)")
st.write("Ask anything based on your PDF knowledge base.")

question = st.text_input("Enter your question:")

if question:
    results = collection.query(query_texts=[question], n_results=5)
    
    docs = results["documents"][0]
    if not docs:
        st.error("No relevant context found.")
    else:
        context = "\n".join(docs)

        with st.spinner("Generating answer ..."):
            prompt = f"""Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Answer:
"""
            response = client.chat.completions.create(
                model="groq-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

            answer = response.choices[0].message.content.strip()
            st.success("### 📘 Answer")
            st.write(answer)

        # Diagram option
        if st.checkbox("Generate RAG Flow Diagram?"):
            keywords = extract_rag_keywords(context)
            pattern = detect_flow_pattern(keywords)
            diagram = generate_rag_flow_diagram(keywords, pattern)

            st.image(diagram)
            st.success("Diagram generated successfully!")

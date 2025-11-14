import streamlit as st
from openai import OpenAI
from rag_retrieve import retrieve
from tutor_prompt import build_tutor_prompt

st.title("📘 RAG AI Tutor")

client = OpenAI()

user_input = st.text_input("Ask something from the document:")
level = st.radio("Explain for:", ["beginner", "developer"])

if user_input:
    chunks = retrieve(user_input)
    context = "\n\n".join(chunks)
    prompt = build_tutor_prompt(user_input, context, level)

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "system", "content": prompt}]
    )

    st.write(response.choices[0].message["content"])

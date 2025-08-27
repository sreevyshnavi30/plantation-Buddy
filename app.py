# app.py
import streamlit as st
from query import query_ollama

st.set_page_config(page_title="Plantation Buddy 🌱", layout="centered")

st.title("🌱 Plantation Buddy")
st.write("Ask me anything about plants, gardening!")

# User input
user_input = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            try:
                answer = query_ollama(user_input)
                st.success(answer)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please type a question before clicking Ask.")

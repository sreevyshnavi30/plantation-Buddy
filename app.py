HEAD
import streamlit as st
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM


# Load ChromaDB with the same embeddings as ingest.py
def load_vectorstore(persist_directory="db"):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectorstore


def main():
    st.set_page_config(page_title="PlantationBuddy 🌱", page_icon="🌿", layout="wide")

    st.title("🌱 PlantationBuddy - RAG Chatbot")
    st.write("Ask me anything about plantation!")

    # Load vectorstore
    vectorstore = load_vectorstore("db")

    # Setup retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Load LLM from Ollama (you can change to mistral, llama2, etc. if available)
    llm = OllamaLLM(model="llama2")

    # Build Retrieval-QA Chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Input box
    query = st.text_input("💬 Ask your question:")

    if query:
        with st.spinner("Thinking... 🤔"):
            result = qa.invoke(query)
            answer = result["result"]
            sources = result["source_documents"]

            # Display answer
            st.markdown("### ✅ Answer")
            st.write(answer)

            # Display sources
            if sources:
                st.markdown("---")
                st.markdown("### 📚 Sources")
                for doc in sources:
                    st.write(f"- {doc.metadata.get('source', 'Unknown source')}")


if __name__ == "__main__":
    main()

import streamlit as st
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM


# Load ChromaDB with the same embeddings as ingest.py
def load_vectorstore(persist_directory="db"):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectorstore


def main():
    st.set_page_config(page_title="PlantationBuddy 🌱", page_icon="🌿", layout="wide")

    st.title("🌱 PlantationBuddy - RAG Chatbot")
    st.write("Ask me anything about the ingested website content!")

    # Load vectorstore
    vectorstore = load_vectorstore("db")

    # Setup retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Load LLM from Ollama (you can change to mistral, llama2, etc. if available)
    llm = OllamaLLM(model="llama2")

    # Build Retrieval-QA Chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # Input box
    query = st.text_input("💬 Ask your question:")

    if query:
        with st.spinner("Thinking... 🤔"):
            result = qa.invoke(query)
            answer = result["result"]
            sources = result["source_documents"]

            # Display answer
            st.markdown("### ✅ Answer")
            st.write(answer)

            # Display sources
            if sources:
                st.markdown("---")
                st.markdown("### 📚 Sources")
                for doc in sources:
                    st.write(f"- {doc.metadata.get('source', 'Unknown source')}")


if __name__ == "__main__":
    main()
56be44e (serve.py)

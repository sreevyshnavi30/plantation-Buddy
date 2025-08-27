import argparse
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="Question to ask the knowledge base")
    parser.add_argument("--persist", type=str, default="db", help="Vector DB folder")
    args = parser.parse_args()

    # Load the same embedding model used during ingest
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Load Chroma DB
    vectorstore = Chroma(persist_directory=args.persist, embedding_function=embeddings)

    # Load LLM (using Ollama locally)
    llm = OllamaLLM(model="llama3")

    # Setup RetrievalQA
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # Run the query
    result = qa.invoke({"query": args.query})
    print("\n✅ Answer:", result["result"])

    print("\n📖 Sources:")
    for doc in result["source_documents"]:
        print("-", doc.metadata.get("source", "Unknown source"))

if __name__ == "__main__":
    main()

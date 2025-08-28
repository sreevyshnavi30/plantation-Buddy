import argparse
from langchain_community.vectorstores import Chroma
from langchain_ollama import Ollama
from langchain.chains import RetrievalQA


def get_args():
    parser = argparse.ArgumentParser(description="Query the Chroma DB with Ollama")
    parser.add_argument("--persist", type=str, default="db", help="Folder where Chroma DB is stored")
    parser.add_argument("--model", type=str, default="mistral", help="Ollama model for answering queries")
    return parser.parse_args()


def main():
    args = get_args()

    # Load Chroma DB
    vectorstore = Chroma(persist_directory=args.persist, embedding_function=None)

    # Use Ollama for text generation
    llm = Ollama(model=args.model)

    # Create a retrieval-based QA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
    )

    print("✅ Ready! Type your questions:")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = qa.run(query)
        print("Bot:", answer)


if __name__ == "__main__":
    main()

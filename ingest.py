import argparse
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings



def get_args():
    parser = argparse.ArgumentParser(description="Ingest data into Chroma with Ollama embeddings")
    parser.add_argument("--urls", type=str, required=True, help="URL of the website to ingest")
    parser.add_argument("--persist", type=str, default="db", help="Folder to store the Chroma DB")
    return parser.parse_args()


def main():
    args = get_args()

    # Load documents from the web
    if args.urls.startswith("http://") or args.urls.startswith("https://"):
        loader = WebBaseLoader(args.urls)
        docs = loader.load()
    else:
        raise ValueError("Please provide a valid URL starting with http:// or https://")

    # Create embeddings using Ollama
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Store in Chroma DB
    vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=args.persist)
    vectorstore.persist()

    print(f"✅ Documents ingested and saved to {args.persist}")


if __name__ == "__main__":
    main()

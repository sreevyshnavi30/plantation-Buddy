# query.py
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

# Initialize Ollama model (make sure you have Ollama running locally)
llm = OllamaLLM(model="llama3")  # You can also use "mistral", "gemma", etc.

# Define a simple prompt template
template = """
You are a helpful assistant for Plantation Buddy.
Answer the user's question clearly.

Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

def query_ollama(question: str) -> str:
    """Send a question to Ollama model and return the response."""
    chain = prompt | llm
    response = chain.invoke({"question": question})
    return response

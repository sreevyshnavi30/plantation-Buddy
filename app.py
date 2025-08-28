from flask import Flask, request, jsonify
from query import run_query

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Welcome to Plantation Buddy 🌱"}

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = run_query(query)
    return jsonify({"query": query, "response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)

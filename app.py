from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask("EchoDocs")

# Load API key from environment
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run to query."

@app.route("/hackrx/run", methods=["POST"])
def ask():
    data = request.get_json()
    document_url = data.get("documents", "")
    questions = data.get("questions", [])

    answers = []

    for q in questions:
        prompt = f"Use this document to answer the question:\nDocument: {document_url}\nQuestion: {q}"
        response = model.generate_content(prompt)
        answers.append(response.text.strip())

    return jsonify({"answers": answers})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

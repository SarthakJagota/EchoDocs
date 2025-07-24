from flask import Flask, request, jsonify
import google.generativeai as genai
app = Flask("EchoDocs")


import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /ask to query."
    
@app.route("/hackrx/run", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    # Optionally load document content here and pass to model
    response = model.generate_content(query)
    return jsonify({
        "answer": response.text.strip()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)





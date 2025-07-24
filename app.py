from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask("EchoDocs")

# ✅ Load Gemini API key from Render environment
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run"

@app.route("/hackrx/run", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        query = data.get("query", "")

        if not query:
            return jsonify({"error": "Missing query in request"}), 400

        response = model.generate_content(query)
        return jsonify({"answer": response.text.strip()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ CORRECTED this line
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

      


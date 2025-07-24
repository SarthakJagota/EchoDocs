from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask("EchoDocs")

# ✅ Set up Gemini
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Home route
@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run to query."

# ✅ Hackathon-compliant POST route
@app.route("/hackrx/run", methods=["POST"])
def run_hackrx():
    data = request.get_json()
    query = data.get("query", "")

    # Optional: parse documents if needed
    documents = data.get("documents", [])

    # Log the documents (for debugging)
    print("Received documents:", documents)

    # 🔥 Generate answer from query
    response = model.generate_content(query)

    return jsonify({
        "answer": response.text.strip()
    })

# ✅ Start server (Render uses this)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

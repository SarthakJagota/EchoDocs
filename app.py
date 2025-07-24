import os
from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import textwrap

app = Flask("EchoDocs")

# ✅ Use secret Gemini key from Render env
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run"

@app.route("/hackrx/run", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        pdf_url = data.get("documents")
        question = data.get("question")  # 💥 only ONE question per request

        if not pdf_url or not question:
            return jsonify({"error": "Missing document or question"}), 400

        # 🧠 Stream PDF + read all pages
        response = requests.get(pdf_url, timeout=10)
        reader = PdfReader(BytesIO(response.content))
        full_text = "\n".join([p.extract_text() or "" for p in reader.pages])

        # 📦 Chunk it small
        chunks = textwrap.wrap(full_text, width=1500)

        # 🔁 Gemini on each chunk
        combined = ""
        for chunk in chunks:
            prompt = f"{chunk}\n\nAnswer this: {question}"
            reply = model.generate_content(prompt)
            combined += reply.text.strip() + "\n"

        return jsonify({"answer": combined.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


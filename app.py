from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import os
import textwrap

app = Flask("EchoDocs")

# ✅ Load API key securely from environment (set this in Render)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run to query."

@app.route("/hackrx/run", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        pdf_url = data.get("documents", "")
        questions = data.get("questions", [])

        if not pdf_url or not questions:
            return jsonify({"error": "Missing document or questions"}), 400

        # 🧠 Download PDF from the URL
        pdf_response = requests.get(pdf_url)
        reader = PdfReader(BytesIO(pdf_response.content))
        full_text = "\n".join([page.extract_text() or "" for page in reader.pages])

        # 🪓 Split into manageable chunks for Gemini
        chunks = textwrap.wrap(full_text, width=2000)

        answers = []
        for question in questions:
            combined_response = ""
            for chunk in chunks:
                prompt = f"Based on the following policy document chunk, answer the question:\n\n{chunk}\n\nQuestion: {question}"
                response = model.generate_content(prompt)
                combined_response += response.text.strip() + "\n"
            answers.append(combined_response.strip())

        return jsonify({"answers": answers})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

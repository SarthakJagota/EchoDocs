from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import google.generativeai as genai
import requests
import os
import tempfile

app = Flask(_name_)

# 👇 Replace with your actual environment variable on Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run to query."

@app.route("/hackrx/run", methods=["POST"])
def ask():
    data = request.get_json()

    pdf_url = data.get("documents")
    questions = data.get("questions", [])

    if not pdf_url or not questions:
        return jsonify({"error": "Missing document or questions"}), 400

    try:
        # ⬇ Download the PDF temporarily
        response = requests.get(pdf_url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(response.content)
            tmp_pdf_path = tmp_pdf.name

        # ⬇ Read PDF content
        reader = PdfReader(tmp_pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # ⬇ Gemini prompt
        prompt = f"""
You are a helpful assistant. Answer the following questions using ONLY the context provided below from the PDF.

📄 CONTEXT:
{text}

❓ QUESTIONS:
"""
        for q in questions:
            prompt += f"- {q}\n"

        gemini_response = model.generate_content(prompt)
        answers = gemini_response.text.strip()

        return jsonify({"answers": answers})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

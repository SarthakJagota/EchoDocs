from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import google.generativeai as genai
import requests
import os
import tempfile
app = Flask(__name__)


# ✅ Use env variable from Render dashboard
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET"])
def home():
    return "✅ EchoDocs server is running. Use POST /hackrx/run to query."

@app.route("/hackrx/run", methods=["POST"])
def hackrx_run():
    data = request.get_json()

    pdf_url = data.get("documents")
    questions = data.get("questions")

    if not pdf_url or not questions:
        return jsonify({"error": "Missing document or questions"}), 400

    try:
        # 📥 Download the PDF
        response = requests.get(pdf_url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            pdf_path = tmp.name

        # 📖 Read text from PDF
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() or ""

        # 🧠 Prepare prompt
        prompt = f"""You are a helpful assistant. Use ONLY the context below to answer the questions:\n\n📄 CONTEXT:\n{full_text}\n\n❓ QUESTIONS:\n"""
        for q in questions:
            prompt += f"- {q}\n"

        gemini_response = model.generate_content(prompt)
        answer = gemini_response.text.strip()

        return jsonify({"answers": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

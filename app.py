import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pdfplumber
import pytesseract
from PIL import Image

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "http://localhost:5000"
SITE_TITLE = "ChatWithPDF"

document_content = ""  # In-memory content

def extract_text(file_path, ext):
    global document_content
    if ext == '.pdf':
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext in ['.png', '.jpg', '.jpeg']:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = ""
    document_content = text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    extract_text(save_path, ext)
    os.remove(save_path)

    return jsonify({'message': 'File processed successfully'})

@app.route('/ask', methods=['POST'])
def ask():
    global document_content
    question = request.json.get('question')

    if not document_content:
        return jsonify({'error': 'No document uploaded'}), 400

    prompt = f"Document Content:\n{document_content[:3000]}\n\nQuestion: {question}\nAnswer:"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_TITLE
    }

    body = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(body))
        result = response.json()

        if response.status_code == 200:
            return jsonify({'answer': result['choices'][0]['message']['content']})
        else:
            return jsonify({'error': result.get('error', {}).get('message', 'Unknown error')}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

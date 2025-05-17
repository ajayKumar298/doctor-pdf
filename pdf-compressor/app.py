from flask import Flask, request, send_file, render_template
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files['pdf']
    target_size = request.form.get('targetSize', type=int)

    if not file or not file.filename.endswith('.pdf'):
        return "Invalid file", 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    compressed_path = os.path.join(COMPRESSED_FOLDER, f"compressed_{filename}")
    file.save(upload_path)

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={compressed_path}",
        upload_path
    ]
    subprocess.run(cmd)

    return send_file(compressed_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
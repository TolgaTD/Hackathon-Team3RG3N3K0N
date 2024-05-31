from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import hashlib
from datetime import datetime
from src.crypt import encrypt_data, generate_keys, split_and_encrypt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ENCRYPTED_FOLDER'] = 'encrypted/'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB limit

nodes = ['node1', 'node2', 'node3', 'node4', 'node5']
for node in nodes:
    os.makedirs(os.path.join(app.config['ENCRYPTED_FOLDER'], node), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        file_data = f.read()
        hash_sha256.update(file_data)
    file_hash = hash_sha256.hexdigest()

    upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    _, public_key = generate_keys()
    encrypted_chunks = split_and_encrypt(file_data, public_key)

    for i, (encrypted_data, iv, encrypted_key) in enumerate(encrypted_chunks):
        node_folder = os.path.join(app.config['ENCRYPTED_FOLDER'], nodes[i])
        encrypted_file_path = os.path.join(node_folder, f'{filename}_part{i}.enc')
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)  # encrypted_data already a bytes-like object

    return jsonify({
        'message': 'File uploaded, encrypted and distributed successfully',
        'filename': filename,
        'hash': file_hash,
        'uploaded_at': upload_time
    }), 200

@app.route('/files')
def list_files():
    files = []
    for node in nodes:
        node_files = os.listdir(os.path.join(app.config['ENCRYPTED_FOLDER'], node))
        for file in node_files:
            files.append({'node': node, 'filename': file})
    return render_template('files.html', files=files)

@app.route('/download/<node>/<filename>', methods=['GET'])
def download_file(node, filename):
    file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], node, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_from_directory(os.path.join(app.config['ENCRYPTED_FOLDER'], node), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

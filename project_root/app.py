from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from src.crypt import generate_keys, encrypt_data, decrypt_data, split_file
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Dosyaların yükleneceği klasör

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Şifreleme anahtarlarını üret
    _, public_key = generate_keys()

    # Dosyayı parçalara böl ve şifrele
    num_chunks = 5
    chunks = split_file(file_path, num_chunks, public_key)

    # Şifrelenmiş parçaları düğümlere dağıt
    distribute_chunks(chunks, filename)

    return jsonify({'message': 'File uploaded and distributed successfully'}), 200

@app.route('/retrieve/<filename>', methods=['GET'])
def retrieve_file(filename):
    chunks = retrieve_chunks_from_nodes(filename)
    private_key, _ = generate_keys()
    file_content = combine_chunks(chunks, private_key)

    return jsonify({'content': file_content.decode()}), 200

def distribute_chunks(chunks, filename):
    # Bu fonksiyon, şifrelenmiş parçaları ağdaki düğümlere gönderir
    nodes = ['node1', 'node2', 'node3', 'node4', 'node5']
    for chunk, node in zip(chunks, nodes):
        print(f'Sending chunk to {node}')  # Gerçek dağıtım burada simüle ediliyor
        with open(f'distributed_{filename}_{node}.chunk', 'wb') as f:
            f.write(chunk)

def retrieve_chunks_from_nodes(filename):
    # Bu fonksiyon düğümlerden şifrelenmiş parçaları geri çeker
    nodes = ['node1', 'node2', 'node3', 'node4', 'node5']
    chunks = []
    for node in nodes:
        chunk_file = f'distributed_{filename}_{node}.chunk'
        if os.path.exists(chunk_file):
            with open(chunk_file, 'rb') as f:
                chunks.append(f.read())
    return chunks

def combine_chunks(chunks, private_key):
    # Parçaları deşifre edip birleştir
    decrypted_chunks = [decrypt_data(chunk, private_key) for chunk in chunks]
    return b''.join(decrypted_chunks)

if __name__ == '__main__':
    app.run(debug=True)

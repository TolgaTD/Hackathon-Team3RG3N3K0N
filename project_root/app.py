from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import hashlib
import json
from time import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)

class DataPiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    piece = db.Column(db.LargeBinary, nullable=False)
    location = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, piece_hash):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'piece_hash': piece_hash,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

blockchain = Blockchain()

def split_file(file_path, chunk_size=1024 * 1024):
    with open(file_path, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            yield chunk
            chunk = f.read(chunk_size)

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

    locations = [f'computer_{i % 3}' for i in range(3)]
    for piece in split_file(file_path):
        location = locations.pop(0)
        piece_hash = hashlib.sha256(piece).hexdigest()
        new_piece = DataPiece(filename=filename, piece=piece, location=location)
        db.session.add(new_piece)
        blockchain.new_transaction(sender="network", recipient=location, piece_hash=piece_hash)
        locations.append(location)
    
    db.session.commit()
    blockchain.new_block(proof=12345)

    return jsonify({'message': 'File uploaded and distributed'}), 201

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    pieces = DataPiece.query.filter_by(filename=filename).all()
    if not pieces:
        return jsonify({'error': 'File not found'}), 404

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'wb') as f:
        for piece in pieces:
            f.write(piece.piece)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)

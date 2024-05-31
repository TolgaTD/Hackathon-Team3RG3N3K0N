import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Anahtarları dosyaya yaz
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("src/private_key.pem", "wb") as key_file:
        key_file.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("src/public_key.pem", "wb") as key_file:
        key_file.write(pem)

    return private_key, public_key

def encrypt_data(data, public_key):
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_data(encrypted_data, private_key):
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted

def split_file(file_path, num_chunks, public_key):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_chunks
    chunks = []
    with open(file_path, 'rb') as file:
        for _ in range(num_chunks - 1):
            chunk = file.read(chunk_size)
            encrypted_chunk = encrypt_data(chunk, public_key)
            chunks.append(encrypted_chunk)
        # Last chunk, to include any leftover
        last_chunk = file.read()
        encrypted_last_chunk = encrypt_data(last_chunk, public_key)
        chunks.append(encrypted_last_chunk)
    return chunks

if __name__ == "__main__":
    private_key, public_key = generate_keys()
    file_path = "path_to_your_large_file.ext"  # Replace this with the path to your file
    num_chunks = 5  # Or any other number depending on how many parts you want to split the file into
    encrypted_chunks = split_file(file_path, num_chunks, public_key)

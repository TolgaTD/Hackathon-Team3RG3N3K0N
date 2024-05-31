import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Anahtarları dosyaya yaz
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("private_key.pem", "wb") as key_file:
        key_file.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("public_key.pem", "wb") as key_file:
        key_file.write(pem)

    return private_key, public_key

def encrypt_data(data, public_key):
    # AES anahtarını rastgele oluştur
    aes_key = os.urandom(32)  # AES için 256-bit anahtar

    # AES şifreleme yap
    iv = os.urandom(16)  # AES için 128-bit IV
    encryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend()).encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # AES anahtarını RSA ile şifrele
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Şifrelenmiş veri ve şifrelenmiş anahtarın her ikisini de döndür
    return encrypted_data, iv, encrypted_key

def decrypt_data(encrypted_data, iv, encrypted_key, private_key):
    # Şifrelenmiş AES anahtarını çöz
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # AES ile veriyi çöz
    decryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend()).decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data

def split_and_encrypt(file_data, public_key):
    chunk_size = len(file_data) // 5
    chunks = [file_data[i * chunk_size:(i + 1) * chunk_size] for i in range(4)]
    chunks.append(file_data[4 * chunk_size:])  # Son parçayı ekle

    encrypted_chunks = []
    for chunk in chunks:
        encrypted_data, iv, encrypted_key = encrypt_data(chunk, public_key)
        encrypted_chunks.append((encrypted_data, iv, encrypted_key))
    return encrypted_chunks


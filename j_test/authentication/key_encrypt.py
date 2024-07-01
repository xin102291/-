from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

# 讀取私鑰文件
with open("my_custom_key.key", "rb") as key_file:
    private_key = key_file.read()

# 生成一個隨機的 32 字節密鑰
password = b"d1051210"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# 使用 AES GCM 進行加密
aesgcm = AESGCM(key)
nonce = os.urandom(12)
encrypted_key = aesgcm.encrypt(nonce, private_key, None)

# 將加密的私鑰寫入文件
with open("my_custom_key_encrypted.key", "wb") as encrypted_file:
    encrypted_file.write(salt + nonce + encrypted_key)
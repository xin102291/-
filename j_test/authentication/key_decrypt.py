from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# 讀取加密的私鑰文件
with open("my_custom_key_encrypted.key", "rb") as encrypted_file:
    data = encrypted_file.read()

# 分離 salt, nonce 和加密的私鑰
salt = data[:16]
nonce = data[16:28]
encrypted_key = data[28:]

# 生成密鑰
password = b"d1051210"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# 使用 AES GCM 進行解密
aesgcm = AESGCM(key)
private_key = aesgcm.decrypt(nonce, encrypted_key, None)

# 將解密的私鑰寫入文件
with open("my_custom_key_decrypted.key", "wb") as decrypted_file:
    decrypted_file.write(private_key)

import base64
import secrets
from typing import Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

def encrypt_file(path: str, password: str) -> str:
    salt = secrets.token_bytes(16)
    key = _derive_key(password, salt)
    f = Fernet(key)
    enc_path = path + ".enc"
    with open(path, "rb") as rf, open(enc_path, "wb") as wf:
        wf.write(b"BKP1" + salt)
        wf.write(f.encrypt(rf.read()))
    return enc_path

def decrypt_file(path: str, password: str, out_path: Optional[str] = None) -> str:
    if out_path is None:
        out_path = path.replace(".enc", "")
    with open(path, "rb") as rf:
        if rf.read(4) != b"BKP1":
            raise ValueError("Formato file non valido (header)")
        salt = rf.read(16)
        key = _derive_key(password, salt)
        token = rf.read()
    data = Fernet(key).decrypt(token)
    with open(out_path, "wb") as wf:
        wf.write(data)
    return out_path

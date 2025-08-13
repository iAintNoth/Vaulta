
import tarfile
import os
from datetime import datetime
from cryptography.fernet import Fernet

def create_backup(source_dir, backup_dir, encrypt_password=""):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tar_path = os.path.join(backup_dir, f"backup_{timestamp}.tar.gz")

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    if encrypt_password:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        with open(tar_path, "rb") as f:
            data = f.read()
        encrypted_data = cipher.encrypt(data)
        with open(tar_path + ".enc", "wb") as f:
            f.write(encrypted_data)
        os.remove(tar_path)
        tar_path += ".enc"
    return tar_path


import paramiko
import os

def upload_sftp(file_path, sftp_config):
    try:
        transport = paramiko.Transport((sftp_config["host"], sftp_config["port"]))
        transport.connect(username=sftp_config["username"], password=sftp_config["password"])
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_path = os.path.join(sftp_config["remote_dir"], os.path.basename(file_path))
        sftp.put(file_path, remote_path)
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(f"Errore upload: {e}")
        return False

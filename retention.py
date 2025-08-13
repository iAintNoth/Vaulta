
import os
import time
import paramiko

def retention_cleanup_local(backup_dir: str, days: int, logger):
    if days <= 0 or not os.path.isdir(backup_dir):
        return
    cutoff = time.time() - days * 86400
    for name in os.listdir(backup_dir):
        path = os.path.join(backup_dir, name)
        if os.path.isfile(path):
            try:
                if os.path.getmtime(path) < cutoff:
                    os.remove(path)
                    logger.info(f"Pulizia (locale): rimosso {path}")
            except Exception as e:
                logger.error(f"Errore pulizia locale su {path}: {e}")

def retention_cleanup_remote(cfg, logger):
    if cfg.retention_days_remote <= 0:
        return
    transport = None
    try:
        transport = paramiko.Transport((cfg.remote_host, cfg.remote_port))
        if cfg.use_password:
            transport.connect(username=cfg.remote_user, password=cfg.remote_password)
        else:
            pkey = None
            if cfg.ssh_key_path:
                try:
                    pkey = paramiko.RSAKey.from_private_key_file(cfg.ssh_key_path)
                except paramiko.PasswordRequiredException:
                    # In GUI si chiede la passphrase quando necessario (vedi upload.py)
                    pass
            transport.connect(username=cfg.remote_user, pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.chdir(cfg.remote_path)
        except IOError:
            return
        cutoff = time.time() - cfg.retention_days_remote * 86400
        for attr in sftp.listdir_attr("."):
            remote_file = f"{cfg.remote_path}/{attr.filename}".replace("\\", "/")
            try:
                if attr.st_mtime < cutoff:
                    sftp.remove(remote_file)
                    logger.info(f"Pulizia (remoto): rimosso {remote_file}")
            except Exception as e:
                logger.error(f"Errore pulizia remoto su {remote_file}: {e}")
        sftp.close()
    finally:
        if transport:
            transport.close()

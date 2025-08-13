import os
import yaml
from pathlib import Path
from typing import Any, Dict

CONFIG_PATH = os.path.join(str(Path.home()), ".backup_pro_app.yaml")

class BackupConfig:
    def __init__(self, **kwargs):
        self.source_dir = kwargs.get("source_dir", "")
        self.local_backup_dir = kwargs.get("local_backup_dir", "")
        self.remote_host = kwargs.get("remote_host", "")
        self.remote_port = int(kwargs.get("remote_port", 22))
        self.remote_user = kwargs.get("remote_user", "")
        self.remote_path = kwargs.get("remote_path", "")
        self.ssh_key_path = kwargs.get("ssh_key_path", "")
        self.use_password = bool(kwargs.get("use_password", False))
        self.remote_password = kwargs.get("remote_password", "")
        self.encrypt = bool(kwargs.get("encrypt", False))
        self.encrypt_password = kwargs.get("encrypt_password", "")
        self.retention_days_local = int(kwargs.get("retention_days_local", 14))
        self.retention_days_remote = int(kwargs.get("retention_days_remote", 30))
        self.schedule_hour = int(kwargs.get("schedule_hour", 2))
        self.schedule_minute = int(kwargs.get("schedule_minute", 0))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_dir": self.source_dir,
            "local_backup_dir": self.local_backup_dir,
            "remote_host": self.remote_host,
            "remote_port": self.remote_port,
            "remote_user": self.remote_user,
            "remote_path": self.remote_path,
            "ssh_key_path": self.ssh_key_path,
            "use_password": self.use_password,
            "remote_password": self.remote_password,
            "encrypt": self.encrypt,
            "encrypt_password": self.encrypt_password,
            "retention_days_local": self.retention_days_local,
            "retention_days_remote": self.retention_days_remote,
            "schedule_hour": self.schedule_hour,
            "schedule_minute": self.schedule_minute,
        }

    @classmethod
    def load(cls, path: str = CONFIG_PATH) -> "BackupConfig":
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return cls(**data)
        return cls()

    def save(self, path: str = CONFIG_PATH):
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, sort_keys=False, allow_unicode=True)

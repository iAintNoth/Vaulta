
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

APP_LOG_DIR = os.path.join(str(Path.home()), ".backup_pro_app_logs")
APP_LOG_FILE = os.path.join(APP_LOG_DIR, "backup.log")
os.makedirs(APP_LOG_DIR, exist_ok=True)

logger = logging.getLogger("BackupProApp")
logger.setLevel(logging.INFO)

_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

_file_handler = RotatingFileHandler(APP_LOG_FILE, maxBytes=2*1024*1024, backupCount=5)
_file_handler.setFormatter(_formatter)
logger.addHandler(_file_handler)

def get_log_file_path() -> str:
    return APP_LOG_FILE


import os
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit, QSpinBox, QTimeEdit
)
from PyQt5.QtCore import QTime

from logger_setup import logger, get_log_file_path
from config import BackupConfig, CONFIG_PATH
from backup import run_backup
from scheduler_module import BackupScheduler

class LogEmitter(QtCore.QObject):
    message = QtCore.pyqtSignal(str)

class QtHandler(QtCore.QObject):
    message = QtCore.pyqtSignal(str)

class BackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup Pro App")
        self.resize(860, 720)

        self.config = BackupConfig.load(CONFIG_PATH)

        layout = QVBoxLayout(self)

        # Source dir
        src_layout = QHBoxLayout()
        self.src_edit = QLineEdit(self.config.source_dir)
        btn_src = QPushButton("Scegli sorgente")
        btn_src.clicked.connect(self.choose_source)
        src_layout.addWidget(QLabel("Sorgente:"))
        src_layout.addWidget(self.src_edit)
        src_layout.addWidget(btn_src)

        # Local backup dir
        dst_layout = QHBoxLayout()
        self.dst_edit = QLineEdit(self.config.local_backup_dir)
        btn_dst = QPushButton("Scegli destinazione")
        btn_dst.clicked.connect(self.choose_backup_dir)
        dst_layout.addWidget(QLabel("Backup locale:"))
        dst_layout.addWidget(self.dst_edit)
        dst_layout.addWidget(btn_dst)

        # Remote 1
        rem_layout1 = QHBoxLayout()
        self.host_edit = QLineEdit(self.config.remote_host)
        self.port_edit = QLineEdit(str(self.config.remote_port))
        self.user_edit = QLineEdit(self.config.remote_user)
        rem_layout1.addWidget(QLabel("Host remoto:"))
        rem_layout1.addWidget(self.host_edit)
        rem_layout1.addWidget(QLabel("Porta:"))
        rem_layout1.addWidget(self.port_edit)
        rem_layout1.addWidget(QLabel("Utente:"))
        rem_layout1.addWidget(self.user_edit)

        # Remote 2
        rem_layout2 = QHBoxLayout()
        self.rempath_edit = QLineEdit(self.config.remote_path)
        self.sshkey_edit = QLineEdit(self.config.ssh_key_path)
        btn_key = QPushButton("Scegli chiave")
        btn_key.clicked.connect(self.choose_key)
        rem_layout2.addWidget(QLabel("Percorso remoto:"))
        rem_layout2.addWidget(self.rempath_edit)
        rem_layout2.addWidget(QLabel("Chiave SSH:"))
        rem_layout2.addWidget(self.sshkey_edit)
        rem_layout2.addWidget(btn_key)

        # Remote 3
        rem_layout3 = QHBoxLayout()
        self.usepass_chk = QCheckBox("Usa password invece di chiave")
        self.usepass_chk.setChecked(self.config.use_password)
        self.pass_edit = QLineEdit(self.config.remote_password)
        self.pass_edit.setEchoMode(QLineEdit.Password)
        rem_layout3.addWidget(self.usepass_chk)
        rem_layout3.addWidget(QLabel("Password SSH:"))
        rem_layout3.addWidget(self.pass_edit)

        # Encryption
        enc_layout = QHBoxLayout()
        self.enc_chk = QCheckBox("Cifra backup")
        self.enc_chk.setChecked(self.config.encrypt)
        self.enc_pass = QLineEdit(self.config.encrypt_password)
        self.enc_pass.setEchoMode(QLineEdit.Password)
        enc_layout.addWidget(self.enc_chk)
        enc_layout.addWidget(QLabel("Password cifratura:"))
        enc_layout.addWidget(self.enc_pass)

        # Retention
        ret_layout = QHBoxLayout()
        self.ret_local = QSpinBox()
        self.ret_local.setRange(0, 3650)
        self.ret_local.setValue(self.config.retention_days_local)
        self.ret_remote = QSpinBox()
        self.ret_remote.setRange(0, 3650)
        self.ret_remote.setValue(self.config.retention_days_remote)
        ret_layout.addWidget(QLabel("Retention locale (giorni):"))
        ret_layout.addWidget(self.ret_local)
        ret_layout.addWidget(QLabel("Retention remoto (giorni):"))
        ret_layout.addWidget(self.ret_remote)

        # Schedule
        sched_layout = QHBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(self.config.schedule_hour, self.config.schedule_minute))
        sched_layout.addWidget(QLabel("Orario giornaliero:"))
        sched_layout.addWidget(self.time_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_run = QPushButton("Esegui backup ora")
        self.btn_run.clicked.connect(self.on_run)
        self.btn_save = QPushButton("Salva configurazione")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_sched = QPushButton("Riavvia scheduler")
        self.btn_sched.clicked.connect(self.restart_scheduler)
        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_sched)

        # Log view
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setLineWrapMode(QTextEdit.NoWrap)

        layout.addLayout(src_layout)
        layout.addLayout(dst_layout)
        layout.addLayout(rem_layout1)
        layout.addLayout(rem_layout2)
        layout.addLayout(rem_layout3)
        layout.addLayout(enc_layout)
        layout.addLayout(ret_layout)
        layout.addLayout(sched_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel(f"Log file: {get_log_file_path()}"))
        layout.addWidget(self.log_view)

        # Scheduler
        self.scheduler = BackupScheduler(lambda: run_backup(self.collect_config(), gui_log_callback=self.append_log))
        self.restart_scheduler()

        self.append_log("Avvio applicazione completato.")

    # ---- UI handlers ----
    def choose_source(self):
        d = QFileDialog.getExistingDirectory(self, "Seleziona cartella sorgente", self.src_edit.text() or str(Path.home()))
        if d:
            self.src_edit.setText(d)

    def choose_backup_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Seleziona cartella di backup", self.dst_edit.text() or str(Path.home()))
        if d:
            self.dst_edit.setText(d)

    def choose_key(self):
        f, _ = QFileDialog.getOpenFileName(self, "Seleziona chiave privata SSH", self.sshkey_edit.text() or str(Path.home()))
        if f:
            self.sshkey_edit.setText(f)

    def on_save(self):
        cfg = self.collect_config()
        from config import CONFIG_PATH
        cfg.save(CONFIG_PATH)
        self.append_log(f"Configurazione salvata in {CONFIG_PATH}")

    def on_run(self):
        cfg = self.collect_config()
        from PyQt5 import QtCore as _QtCore
        from PyQt5.QtWidgets import QApplication
        QApplication.setOverrideCursor(_QtCore.Qt.WaitCursor)
        try:
            run_backup(cfg, gui_log_callback=self.append_log)
        finally:
            QApplication.restoreOverrideCursor()

    def append_log(self, msg: str):
        self.log_view.append(msg)

    def restart_scheduler(self):
        t = self.time_edit.time()
        self.scheduler.start_daily(t.hour(), t.minute())
        self.append_log(f"Scheduler attivo: ogni giorno alle {t.hour():02d}:{t.minute():02d}")

    def collect_config(self) -> BackupConfig:
        t = self.time_edit.time()
        from config import BackupConfig
        return BackupConfig(
            source_dir=self.src_edit.text().strip(),
            local_backup_dir=self.dst_edit.text().strip(),
            remote_host=self.host_edit.text().strip(),
            remote_port=int(self.port_edit.text() or "22"),
            remote_user=self.user_edit.text().strip(),
            remote_path=self.rempath_edit.text().strip(),
            ssh_key_path=self.sshkey_edit.text().strip(),
            use_password=self.usepass_chk.isChecked(),
            remote_password=self.pass_edit.text(),
            encrypt=self.enc_chk.isChecked(),
            encrypt_password=self.enc_pass.text(),
            retention_days_local=int(self.ret_local.value()),
            retention_days_remote=int(self.ret_remote.value()),
            schedule_hour=t.hour(),
            schedule_minute=t.minute(),
        )


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QSpinBox, QTextEdit, QHBoxLayout
from config_manager import load_config, save_config
from backup import create_backup
from upload import upload_sftp

class BackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup Pro Configurable")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.config = load_config()

        # Campi configurazione
        self.source_edit = self.add_file_field("Cartella sorgente", self.config.get("source_dir", ""))
        self.dest_edit = self.add_file_field("Cartella destinazione", self.config.get("backup_dir", ""))
        self.pass_edit = self.add_text_field("Password cifratura", self.config.get("encrypt_password", ""), True)

        self.sftp_host = self.add_text_field("SFTP Host", self.config.get("sftp", {}).get("host", ""))
        self.sftp_port = self.add_spin_field("SFTP Porta", self.config.get("sftp", {}).get("port", 22))
        self.sftp_user = self.add_text_field("SFTP Username", self.config.get("sftp", {}).get("username", ""))
        self.sftp_pass = self.add_text_field("SFTP Password", self.config.get("sftp", {}).get("password", ""), True)
        self.sftp_dir = self.add_text_field("SFTP Remote Dir", self.config.get("sftp", {}).get("remote_dir", ""))

        self.retention_days = self.add_spin_field("Retention giorni", self.config.get("retention_days", 3))

        # Pulsanti
        save_btn = QPushButton("Salva Configurazione")
        save_btn.clicked.connect(self.save_config)
        self.layout.addWidget(save_btn)

        backup_btn = QPushButton("Esegui Backup")
        backup_btn.clicked.connect(self.run_backup)
        self.layout.addWidget(backup_btn)

        # Log
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.layout.addWidget(self.log_box)

    def add_file_field(self, label, value):
        self.layout.addWidget(QLabel(label))
        hl = QHBoxLayout()
        edit = QLineEdit(value)
        browse_btn = QPushButton("Sfoglia")
        browse_btn.clicked.connect(lambda: edit.setText(QFileDialog.getExistingDirectory(self, "Seleziona cartella")))
        hl.addWidget(edit)
        hl.addWidget(browse_btn)
        self.layout.addLayout(hl)
        return edit

    def add_text_field(self, label, value, password=False):
        self.layout.addWidget(QLabel(label))
        edit = QLineEdit(value)
        if password:
            edit.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(edit)
        return edit

    def add_spin_field(self, label, value):
        self.layout.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setMaximum(9999)
        spin.setValue(value)
        self.layout.addWidget(spin)
        return spin

    def save_config(self):
        self.config = {
            "source_dir": self.source_edit.text(),
            "backup_dir": self.dest_edit.text(),
            "encrypt_password": self.pass_edit.text(),
            "sftp": {
                "host": self.sftp_host.text(),
                "port": self.sftp_port.value(),
                "username": self.sftp_user.text(),
                "password": self.sftp_pass.text(),
                "remote_dir": self.sftp_dir.text(),
            },
            "retention_days": self.retention_days.value()
        }
        save_config(self.config)
        self.log_box.append("Configurazione salvata.")

    def run_backup(self):
        self.save_config()
        self.log_box.append("Avvio backup...")
        backup_path = create_backup(self.config["source_dir"], self.config["backup_dir"], self.config["encrypt_password"])
        self.log_box.append(f"Backup creato: {backup_path}")
        if upload_sftp(backup_path, self.config["sftp"]):
            self.log_box.append("Upload completato con successo.")
        else:
            self.log_box.append("Errore nell'upload.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackupApp()
    window.show()
    sys.exit(app.exec_())

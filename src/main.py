import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QTextEdit, QFileDialog, QMessageBox
)

from src.cipher_service import hide_message, reveal_message


class VishantiCipher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vishanti Cipher")
        self.resize(400, 450)

        self.image_path = ""

        layout = QVBoxLayout()

        self.image_label = QLabel("No image selected")
        layout.addWidget(self.image_label)

        select_button = QPushButton("Select Image")
        select_button.clicked.connect(self.select_image)
        layout.addWidget(select_button)

        layout.addWidget(QLabel("Message:"))

        self.message = QTextEdit()
        self.message.setPlaceholderText("Enter message or view recovered message")
        layout.addWidget(self.message)

        layout.addWidget(QLabel("Password:"))

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        hide_button = QPushButton("Encrypt & Hide")
        hide_button.clicked.connect(self.hide_message)
        layout.addWidget(hide_button)

        reveal_button = QPushButton("Reveal Message")
        reveal_button.clicked.connect(self.reveal_message)
        layout.addWidget(reveal_button)

        self.setLayout(layout)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if path:
            self.image_path = path
            self.image_label.setText(path)

    def hide_message(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Select an image first.")
            return

        message = self.message.toPlainText()
        password = self.password.text()

        if not message or not password:
            QMessageBox.warning(
                self, "Error", "Enter both message and password."
            )
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Stego Image",
            "encrypted_image.png",
            "PNG Images (*.png)"
        )

        if not output_path:
            return

        if not output_path.lower().endswith(".png"):
            output_path += ".png"

        try:
            hide_message(
                self.image_path,
                output_path,
                message,
                password
            )
            QMessageBox.information(
                self, "Success", "Message hidden successfully."
            )
        except Exception as error:
            QMessageBox.critical(self, "Error", str(error))

    def reveal_message(self):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Select an image first.")
            return

        password = self.password.text()

        if not password:
            QMessageBox.warning(self, "Error", "Enter the password.")
            return

        try:
            message = reveal_message(self.image_path, password)
            self.message.setPlainText(message)
            QMessageBox.information(
                self, "Success", "Message recovered successfully."
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not recover the message.\n\n"
                f"Error type: {type(error).__name__}\n"
                f"Details: {error}"
            )


app = QApplication(sys.argv)
window = VishantiCipher()
window.show()
sys.exit(app.exec())

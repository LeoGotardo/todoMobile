from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from socket_client import SocketClient


class RegisterScreen(QWidget):
    def __init__(self, on_register_success):
        super().__init__()

        self.on_register_success = on_register_success

        self.setWindowTitle("Registro - Todo App")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Email:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Registrar")
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            client = SocketClient()
            response = client.send_and_receive({
                "type": "createUser",
                "username": username,
                "password": password
            })

            if response.get("success"):
                QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
                self.on_register_success()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", response.get("error", "Falha no registro."))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro de conexão:\n{str(e)}")

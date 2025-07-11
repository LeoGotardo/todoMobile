from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout
from socket_client import SocketClient


class LoginScreen(QWidget):
    def __init__(self, on_login_success, on_register):
        super().__init__()

        self.on_login_success = on_login_success
        self.on_register = on_register

        self.setWindowTitle("Login - Todo App")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Registrar")
        self.register_button.clicked.connect(self.handle_register)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_login(self):
        username = self.email_input.text()
        password = self.password_input.text()

        try:
            client = SocketClient()
            response = client.send_and_receive({
                "type": "login",
                "username": username,
                "password": password
            })

            if response.get("success"):
                QMessageBox.information(self, "Sucesso", "Login bem-sucedido!")
                self.on_login_success(response.get("userId"))
                self.close()
            else:
                QMessageBox.warning(self, "Erro", response.get("error", "Falha no login."))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro de conexão:\n{str(e)}")

    def handle_register(self):
        self.close()
        self.on_register()
# main.py
import sys
from PySide6.QtWidgets import QApplication
from loginScreen import LoginScreen
from todo_screen import TodoScreen
from registerScreen import RegisterScreen


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Armazena referências das janelas
        self.login = None
        self.register = None
        self.todo = None

        self.show_login_screen()

    def show_login_screen(self):
        self.login = LoginScreen(
            on_login_success=self.show_todo_screen,
            on_register=self.show_register_screen
        )
        self.login.show()

    def show_todo_screen(self, user_id):
        self.todo = TodoScreen(user_id)
        self.todo.show()

    def show_register_screen(self):
        self.register = RegisterScreen(
            on_register_success=self.show_login_screen
        )
        self.register.show()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    MainApp().run()

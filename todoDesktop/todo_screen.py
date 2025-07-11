from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QListWidgetItem
from socket_client import SocketClient


class TodoScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.setWindowTitle("Tarefas - Socket")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout()

        self.todo_list = QListWidget()
        layout.addWidget(self.todo_list)

        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Nova tarefa")
        layout.addWidget(self.todo_input)

        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_todo)
        layout.addWidget(add_button)

        refresh_button = QPushButton("Atualizar")
        refresh_button.clicked.connect(self.load_todos)
        layout.addWidget(refresh_button)

        close_button = QPushButton("Fechar App")
        close_button.clicked.connect(self.close_app)
        layout.addWidget(close_button)

        self.setLayout(layout)

        self.load_todos()

    def load_todos(self):
        client = SocketClient()
        response = client.send_and_receive({
            "type": "getTodos",
            "userId": self.user_id
        })

        self.todo_list.clear()
        if response.get("success"):
            todos = response.get("todos", [])
            for todo in todos:
                item = QListWidgetItem(f"[{'✔' if todo.get('done') else ' '}] {todo.get('title')}")
                self.todo_list.addItem(item)
        else:
            QMessageBox.warning(self, "Erro", response.get("error", "Erro ao carregar tarefas."))

    def add_todo(self):
        title = self.todo_input.text()
        if not title:
            return

        client = SocketClient()
        response = client.send_and_receive({
            "type": "createTodo",
            "userId": self.user_id,
            "title": title
        })

        if response.get("success"):
            self.todo_input.clear()
            self.load_todos()
        else:
            QMessageBox.warning(self, "Erro", response.get("error", "Erro ao criar tarefa."))

    def close_app(self):
        self.close()

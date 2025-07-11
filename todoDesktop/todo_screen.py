from PySide6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QPushButton, 
                               QLineEdit, QMessageBox, QListWidgetItem, QHBoxLayout,
                               QDialog, QTextEdit, QDialogButtonBox, QLabel,
                               QMenu, QInputDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from socket_client import SocketClient
import json


class EditTodoDialog(QDialog):
    def __init__(self, todo_data, parent=None):
        super().__init__(parent)
        self.todo_data = todo_data
        
        self.setWindowTitle("Editar Tarefa")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Título:"))
        self.title_input = QLineEdit()
        self.title_input.setText(todo_data.get('title', ''))
        layout.addWidget(self.title_input)
        
        layout.addWidget(QLabel("Descrição:"))
        self.description_input = QTextEdit()
        self.description_input.setText(todo_data.get('description', ''))
        self.description_input.setMaximumHeight(100)
        layout.addWidget(self.description_input)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self):
        return {
            "title": self.title_input.text(),
            "description": self.description_input.toPlainText()
        }


class TodoScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.todos_data = []  

        self.setWindowTitle("Minhas Tarefas")
        self.setFixedSize(500, 600)

        layout = QVBoxLayout()

        self.todo_list = QListWidget()
        self.todo_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_context_menu)
        self.todo_list.itemDoubleClicked.connect(self.toggle_todo_status)
        layout.addWidget(self.todo_list)

        input_layout = QHBoxLayout()
        
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Nova tarefa...")
        self.todo_input.returnPressed.connect(self.add_todo)
        input_layout.addWidget(self.todo_input)

        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.add_todo)
        input_layout.addWidget(add_button)
        
        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()

        clear_completed_button = QPushButton("Limpar Concluídas")
        clear_completed_button.clicked.connect(self.clear_completed_todos)
        button_layout.addWidget(clear_completed_button)

        logout_button = QPushButton("Sair")
        logout_button.clicked.connect(self.logout)
        button_layout.addWidget(logout_button)
        
        layout.addLayout(button_layout)

        self.status_label = QLabel("Carregando tarefas...")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        
        self.load_todos()

    def load_todos(self):
        client = SocketClient()
        response = client.send_and_receive({
            "type": "getTodos",
            "userId": self.user_id
        })

        self.todo_list.clear()
        self.todos_data = []
        
        if response.get("success"):
            todos = response.get("todos", [])
            self.todos_data = todos
            
            completed_count = 0
            for todo in todos:
                if todo.get('done'):
                    item_text = f"✓ {todo.get('title')} (Concluída)"
                    completed_count += 1
                else:
                    item_text = f"○ {todo.get('title')}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, todo.get('id'))
                
                if todo.get('done'):
                    font = item.font()
                    font.setStrikeOut(True)
                    item.setFont(font)
                    item.setForeground(Qt.gray)
                
                self.todo_list.addItem(item)
            
            total = len(todos)
            pending = total - completed_count
            self.status_label.setText(f"Total: {total} | Pendentes: {pending} | Concluídas: {completed_count}")
        else:
            QMessageBox.warning(self, "Erro", response.get("error", "Erro ao carregar tarefas."))
            self.status_label.setText("Erro ao carregar tarefas")

    def add_todo(self):
        title = self.todo_input.text().strip()
        if not title:
            return

        client = SocketClient()
        response = client.send_and_receive({
            "type": "createTodo",
            "userId": self.user_id,
            "title": title,
            "description": ""
        })

        if response.get("success"):
            self.todo_input.clear()
            self.load_todos()
            QMessageBox.information(self, "Sucesso", "Tarefa adicionada!")
        else:
            QMessageBox.warning(self, "Erro", response.get("error", "Erro ao criar tarefa."))

    def show_context_menu(self, position):
        item = self.todo_list.itemAt(position)
        if not item:
            return
        
        todo_id = item.data(Qt.UserRole)
        todo_data = next((t for t in self.todos_data if t['id'] == todo_id), None)
        if not todo_data:
            return

        menu = QMenu(self)

        if todo_data.get('done'):
            toggle_action = QAction("Marcar como Pendente", self)
        else:
            toggle_action = QAction("Marcar como Concluída", self)
        toggle_action.triggered.connect(lambda: self.toggle_todo_status(item))
        menu.addAction(toggle_action)
        
        edit_action = QAction("Editar", self)
        edit_action.triggered.connect(lambda: self.edit_todo(todo_id))
        menu.addAction(edit_action)
        
        delete_action = QAction("Excluir", self)
        delete_action.triggered.connect(lambda: self.delete_todo(todo_id))
        menu.addAction(delete_action)
        
        menu.exec_(self.todo_list.mapToGlobal(position))

    def toggle_todo_status(self, item):
        todo_id = item.data(Qt.UserRole)
        todo_data = next((t for t in self.todos_data if t['id'] == todo_id), None)
        if not todo_data:
            return
        
        new_status = 0 if todo_data.get('done') else 1
        
        client = SocketClient()
        response = client.send_and_receive({
            "type": "updateTodo",
            "todoId": todo_id,
            "done": new_status
        })
        
        if response.get("success"):
            self.load_todos()
        else:
            QMessageBox.warning(self, "Erro", response.get("error", "Erro ao atualizar tarefa."))

    def edit_todo(self, todo_id):
        todo_data = next((t for t in self.todos_data if t['id'] == todo_id), None)
        if not todo_data:
            return
        
        dialog = EditTodoDialog(todo_data, self)
        if dialog.exec_():
            new_data = dialog.get_data()
            
            client = SocketClient()
            response = client.send_and_receive({
                "type": "updateTodo",
                "todoId": todo_id,
                "title": new_data["title"],
                "description": new_data["description"]
            })
            
            if response.get("success"):
                self.load_todos()
                QMessageBox.information(self, "Sucesso", "Tarefa atualizada!")
            else:
                QMessageBox.warning(self, "Erro", response.get("error", "Erro ao atualizar tarefa."))

    def delete_todo(self, todo_id):
        reply = QMessageBox.question(
            self, 
            "Confirmar Exclusão", 
            "Tem certeza que deseja excluir esta tarefa?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            client = SocketClient()
            response = client.send_and_receive({
                "type": "deleteTodo",
                "todoId": todo_id
            })
            
            if response.get("success"):
                self.load_todos()
                QMessageBox.information(self, "Sucesso", "Tarefa excluída!")
            else:
                QMessageBox.warning(self, "Erro", response.get("error", "Erro ao excluir tarefa."))

    def clear_completed_todos(self):
        completed_todos = [t for t in self.todos_data if t.get('done')]
        
        if not completed_todos:
            QMessageBox.information(self, "Info", "Não há tarefas concluídas para remover.")
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirmar Limpeza", 
            f"Deseja remover {len(completed_todos)} tarefa(s) concluída(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            errors = 0
            for todo in completed_todos:
                client = SocketClient()
                response = client.send_and_receive({
                    "type": "deleteTodo",
                    "todoId": todo['id']
                })
                if not response.get("success"):
                    errors += 1
            
            self.load_todos()
            
            if errors == 0:
                QMessageBox.information(self, "Sucesso", "Tarefas concluídas removidas!")
            else:
                QMessageBox.warning(self, "Aviso", f"Algumas tarefas não puderam ser removidas ({errors} erros).")

    def logout(self):
        reply = QMessageBox.question(
            self, 
            "Confirmar Saída", 
            "Deseja realmente sair?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()

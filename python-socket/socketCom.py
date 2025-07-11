import socket, os, sys, json, requests
from database import User, Todo, Database

class SocketCom:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        if isinstance(data, str):
            self.socket.send(data.encode())
        else:
            self.socket.send(data)

    def receive(self):
        return self.socket.recv(1024).decode()

    def close(self):
        self.socket.close()

    def sendData(self, data):
        self.send(json.dumps(data))

    def receiveData(self):
        return json.loads(self.receive())


class SocketComServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.database = Database()

    def close(self):
        self.socket.close()

    def run(self):
        print(f"Servidor rodando em {self.host}:{self.port}")
        while True:
            try:
                connection, client_address = self.socket.accept()
                print("Conexão de", client_address)
                
                data = connection.recv(4096)
                if data:
                    try:
                        data = json.loads(data.decode())
                        print(f"Requisição: {data.get('type')}")
                        
                        response = {"success": False, "error": "Tipo não reconhecido"}
                        
                        if data["type"] == "login":
                            response = self.login(data)
                        elif data["type"] == "logout":
                            response = self.logout(data)
                        elif data["type"] == "createUser":
                            response = self.createUser(data)
                        elif data["type"] == "deleteUser":
                            response = self.deleteUser(data)
                        elif data["type"] == "getUsers":
                            response = self.getUsers(data)
                        elif data["type"] == "updateUser":
                            response = self.updateUser(data)
                        elif data["type"] == "createTodo":
                            response = self.createTodo(data)
                        elif data["type"] == "deleteTodo":
                            response = self.deleteTodo(data)
                        elif data["type"] == "getTodos":
                            response = self.getTodos(data)
                        elif data["type"] == "updateTodo":
                            response = self.updateTodo(data)
                        elif data["type"] == "getAllTodos":
                            response = self.getAllTodos(data)
                        elif data["type"] == "getUserTodos":
                            response = self.getUserTodos(data)
                        
                        connection.send(json.dumps(response).encode())
                        
                    except json.JSONDecodeError:
                        error_resp = {"success": False, "error": "JSON inválido"}
                        connection.send(json.dumps(error_resp).encode())
                    except Exception as e:
                        error_resp = {"success": False, "error": str(e)}
                        connection.send(json.dumps(error_resp).encode())
                        print(f"Erro processando requisição: {e}")
                
                connection.close()
                
            except Exception as e:
                print(f"Erro no servidor: {e}")

    def login(self, data):
        try:
            username = data.get("username")
            password = data.get("password")
            
            success, result = self.database.loginUser(username, password)
            
            if success:
                return {
                    "success": True,
                    "userId": result.id,
                    "username": result.username
                }
            else:
                return {"success": False, "error": str(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def logout(self, data):
        return {"success": True, "message": "Logout realizado"}

    def createUser(self, data):
        try:
            username = data.get("username")
            password = data.get("password")
            
            success, result = self.database.addUser(username, password)
            
            if success:
                return {
                    "success": True,
                    "userId": result.id,
                    "message": "Usuário criado com sucesso"
                }
            else:
                return {"success": False, "error": str(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def deleteUser(self, data):
        try:
            user_id = data.get("userId")
            
            success, result = self.database.deleteUser(user_id)
            
            if success:
                return {"success": True, "message": "Usuário excluído"}
            else:
                return {"success": False, "error": str(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def getUsers(self, data):
        return {"success": False, "error": "Método não implementado"}

    def updateUser(self, data):
        try:
            user_id = data.get("userId")
            username = data.get("username")
            password = data.get("password")
            
            success, result = self.database.editUser(user_id, username, password)
            
            if success:
                return {"success": True, "message": "Usuário atualizado"}
            else:
                return {"success": False, "error": str(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def getTodos(self, data):
        try:
            user_id = data.get("userId")
            
            success, todos = self.database.getUserTodos(user_id)
            
            if success:
                todos_list = []
                for todo in todos:
                    todos_list.append({
                        "id": todo.id,
                        "title": todo.title,
                        "description": todo.description,
                        "done": bool(todo.done),
                        "due_date": todo.due_date.isoformat() if todo.due_date else None,
                        "created_at": todo.created_at.isoformat() if todo.created_at else None
                    })
                return {"success": True, "todos": todos_list}
            else:
                return {"success": False, "error": str(todos)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def createTodo(self, data):
        try:
            title = data.get("title")
            description = data.get("description", "")
            due_date = data.get("due_date", None)
            owner_id = data.get("userId")
            
            success, result = self.database.addTodo(
                title=title,
                description=description,
                due_date=due_date,
                ownerId=owner_id
            )
            
            if success:
                return {
                    "success": True,
                    "todoId": result.id,
                    "message": "Tarefa criada com sucesso"
                }
            else:
                return {"success": False, "error": str(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def updateTodo(self, data):
        try:
            todo_id = data.get("todoId")
            title = data.get("title")
            description = data.get("description")
            due_date = data.get("due_date")
            done = data.get("done")

            success, todo = self.database.getTodo(todo_id)
            if not success:
                return {"success": False, "error": "Tarefa não encontrada"}
 
            if done is not None:
                try:
                    todo.done = int(done)
                    self.database.session.commit()
                except Exception as e:
                    self.database.session.rollback()
                    return {"success": False, "error": f"Erro ao atualizar status: {str(e)}"}

            if title or description or due_date:
                success, result = self.database.editTodo(
                    todoiId=todo_id,
                    title=title,
                    description=description,
                    due_date=due_date
                )
                
                if not success:
                    return {"success": False, "error": str(result)}
            
            return {"success": True, "message": "Tarefa atualizada"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def deleteTodo(self, data):
        try:
            todo_id = data.get("todoId")
            
            success, result = self.database.deleteTodo(todo_id)
            
            if success:
                return {"success": True, "message": "Tarefa excluída"}
            else:
                return {"success": False, "error": str(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def getAllTodos(self, data):
        return {"success": False, "error": "Método não implementado"}

    def getUserTodos(self, data):
        return self.getTodos(data)

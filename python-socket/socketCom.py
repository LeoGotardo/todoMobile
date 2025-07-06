import socket, os, sys, json, requests

from database import User, Todo, Database


class SocketCom:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(data)

    def receive(self):
        return self.socket.recv(1024)

    def close(self):
        self.socket.close()

    def sendData(self, data):
        self.send(json.dumps(data))

    def receiveData(self):
        return json.loads(self.receive())

    def sendDataToUser(self, user, data):
        self.sendData({"user": user, "data": data})

    def receiveDataFromUser(self, user):
        data = self.receiveData()
        if data["user"] == user:
            return data["data"]
        else:
            return None

    def sendDataToAll(self, data):
        self.sendData({"all": data})        

    def receiveDataFromAll(self):
        data = self.receiveData()
        if data["all"]:
            return data["all"]
        else:
            return None

    def sendDataToTodo(self, todo, data):
        self.sendData({"todo": todo, "data": data})

    def receiveDataFromTodo(self, todo):
        data = self.receiveData()
        if data["todo"] == todo:
            return data["data"]
        else:
            return None

    def sendDataToAllTodos(self, data):
        self.sendData({"allTodos": data})

    def receiveDataFromAllTodos(self):
        data = self.receiveData()
        if data["allTodos"]:
            return data["allTodos"]
        else:
            return None

    def sendDataToUserTodos(self, user, data):
        self.sendData({"userTodos": user, "data": data})

    def receiveDataFromUserTodos(self, user):
        data = self.receiveData()
        if data["userTodos"] == user:
            return data["data"]
        else:
            return None


class SocketComServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

        self.database = Database()

        self.users = {}

        self.todos = {}

    def close(self):
        self.socket.close()

    def run(self):
        while True:
            connection, client_address = self.socket.accept()
            print("Connection from", client_address)
            data = connection.recv(1024)
            if data:
                data = json.loads(data)
                if data["type"] == "login":
                    self.login(connection, data)
                elif data["type"] == "logout":
                    self.logout(connection, data)
                elif data["type"] == "createUser":
                    self.createUser(connection, data)
                elif data["type"] == "deleteUser":
                    self.deleteUser(connection, data)
                elif data["type"] == "getUsers":
                    self.getUsers(connection, data)
                elif data["type"] == "updateUser":
                    self.updateUser(connection, data)
                elif data["type"] == "createTodo":
                    self.createTodo(connection, data)
                elif data["type"] == "deleteTodo":
                    self.deleteTodo(connection, data)
                elif data["type"] == "getTodos":
                    self.getTodos(connection, data)                    
                elif data["type"] == "updateTodo":
                    self.updateTodo(connection, data)
                elif data["type"] == "getAllTodos":
                    self.getAllTodos(connection, data)
                elif data["type"] == "getUserTodos":
                    self.getUserTodos(connection, data)
                else:
                    print("Unknown type")
            connection.close()

    def login(self, connection, data):
        user = User(data["user"])
        if user.exists():
            self.users[user.id] = user
            connection.send(json.dumps({"type": "login", "user": user.id}))
            print("Login OK")
        else:
            connection.send(json.dumps({"type": "login", "error": "User does not exist"}))
            print("Login error")

    def logout(self, connection, data):
        user = User(data["user"])
        if user.exists():
            del self.users[user.id]
            connection.send(json.dumps({"type": "logout", "user": user.id}))
            print("Logout OK")
        else:
            connection.send(json.dumps({"type": "logout", "error": "User does not exist"}))
            print("Logout error")

    def createUser(self, connection, data):
        user = User(data["user"])
        if user.exists():
            connection.send(json.dumps({"type": "createUser", "error": "User already exists"}))
            print("Create user error")
        else:
            user.save()
            self.users[user.id] = user
            connection.send(json.dumps({"type": "createUser", "user": user.id}))
            print("Create user OK")

    def deleteUser(self, connection, data):
        user = User(data["user"])
        if user.exists():
            user.delete()
            del self.users[user.id]
            connection.send(json.dumps({"type": "deleteUser", "user": user.id}))
            print("Delete user OK")
        else:
            connection.send(json.dumps({"type": "deleteUser", "error": "User does not exist"}))
            print("Delete user error")
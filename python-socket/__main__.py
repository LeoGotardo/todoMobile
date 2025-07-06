from socketCom import SocketComServer
from database import Database, User, Todo

def main():
    database = Database()
    socket = SocketComServer("127.0.0.1", 8080).run()
    

if __name__ == "__main__":
    main()

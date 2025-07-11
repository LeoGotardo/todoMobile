import socket
import json

class SocketClient:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.sock = None

    def send_and_receive(self, data: dict) -> dict:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))  
                sock.sendall(json.dumps(data).encode())
                response_data = sock.recv(4096)
                return json.loads(response_data.decode())
        except Exception as e:
            print(f"Erro de socket: {e}")
            return {"success": False, "error": str(e)}
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import socket

app = Flask(__name__)
CORS(app) 

class SocketClientWrapper:
    def __init__(self, host='192.168.0.29', port=8080):
        self.host = host
        self.port = port
    
    def send_and_receive(self, data):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            client_socket.send(json.dumps(data).encode())
            
            response = client_socket.recv(4096).decode()
            client_socket.close()
            
            return json.loads(response)
        except Exception as e:
            return {"success": False, "error": str(e)}

@app.route('/', methods=['POST'])
def handle_request():
    try:
        data = request.get_json()
        
        client = SocketClientWrapper()
        response = client.send_and_receive(data)
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("Servidor HTTP rodando na porta 5000")
    print("Certifique-se de que o servidor Socket está rodando na porta 8081")
    app.run(host='0.0.0.0', port=5000, debug=True)

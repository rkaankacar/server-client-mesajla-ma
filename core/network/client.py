import socket, threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send(self, message):
        self.client_socket.sendall(message.encode())

    def start_receiving(self, handler):
        threading.Thread(target=self._receive, args=(handler,), daemon=True).start()

    def _receive(self, handler):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                handler(data)
            except:
                break

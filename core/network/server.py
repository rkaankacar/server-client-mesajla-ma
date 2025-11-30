import socket, threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []

    
        self.plain_messages = []    
 
        self.encrypted_messages = []  

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.port = self.server_socket.getsockname()[1]
        self.server_socket.listen()

    def start(self, message_handler):
        threading.Thread(target=self._accept_clients, args=(message_handler,), daemon=True).start()

    def _accept_clients(self, handler):
        while True:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            threading.Thread(target=self._handle_client, args=(conn, addr, handler), daemon=True).start()

    def _handle_client(self, conn, addr, handler):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                
              
                self.encrypted_messages.append(data)
                
              
                handler(addr, data)  
            except:
                break
        conn.close()
        if conn in self.clients:
            self.clients.remove(conn)

    def send(self, text):
        """
        Bu fonksiyon Server'dan tüm Client'lara mesaj yollar.
        """
        for c in self.clients:
            try:
                c.sendall(text.encode())
            except:
                pass
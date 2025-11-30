import socket
import threading

from core.encryption.encryption_factory import EncryptionFactory

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send(self, message):
        """Bu fonksiyon sadece veriyi yollar (Raw send)."""
        self.client_socket.sendall(message.encode())

    def send_encrypted(self, message, algo_type, **kwargs):
        """
        Mesajı seçilen algoritmaya göre şifreler ve öyle gönderir.
        Kullanımı: client.send_encrypted("Selam", "Sezar", shift=5)
        """
        try:
        
            cipher = EncryptionFactory.get_cipher(algo_type, **kwargs)
            
        
            encrypted_message = cipher.encrypt(message)
            
           
            print(f"[Client] '{message}' -> '{encrypted_message}' olarak şifrelenip gönderildi.")
            
            self.send(encrypted_message)
        except Exception as e:
            print(f"Şifreleme hatası: {e}")

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
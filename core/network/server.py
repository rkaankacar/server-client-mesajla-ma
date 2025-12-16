<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Chat Server - RSA Key Exchange destekli
"""

import socket
import threading
import json

from core.network.key_exchange import KeyExchangeServer, is_key_exchange_message

=======
import socket, threading
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
<<<<<<< HEAD
        self.client_info = {}  # {conn: {"addr": addr, "key_exchange": KeyExchangeServer, "symmetric_key": bytes}}
        
        self.plain_messages = []
        self.encrypted_messages = []
        
        # Key Exchange durumu
        self.key_exchange_enabled = True
        self.default_algo = "AES"  # Varsayılan simetrik algoritma
        
=======

    
        self.plain_messages = []    
 
        self.encrypted_messages = []  

>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
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
<<<<<<< HEAD
            
            # Her client için key exchange yöneticisi oluştur
            key_ex = KeyExchangeServer(2048)
            self.client_info[conn] = {
                "addr": addr,
                "key_exchange": key_ex,
                "symmetric_key": None,
                "symmetric_algo": None,
                "handshake_done": False
            }
            
            # Key Exchange başlat - public key gönder
            if self.key_exchange_enabled:
                try:
                    handshake = key_ex.create_handshake_message()
                    conn.sendall(handshake.encode())
                    print(f"[Server] Key Exchange başlatıldı: {addr}")
                except Exception as e:
                    print(f"[Server] Handshake hatası: {e}")
            
=======
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
            threading.Thread(target=self._handle_client, args=(conn, addr, handler), daemon=True).start()

    def _handle_client(self, conn, addr, handler):
        while True:
            try:
<<<<<<< HEAD
                data = conn.recv(4096).decode()
                if not data:
                    break
                
                # Key Exchange mesajı mı kontrol et
                if is_key_exchange_message(data):
                    self._process_key_exchange(conn, data)
                else:
                    # Normal şifreli mesaj
                    self.encrypted_messages.append(data)
                    handler(addr, data)
                    
            except Exception as e:
                print(f"[Server] Hata: {e}")
                break
                
        conn.close()
        if conn in self.clients:
            self.clients.remove(conn)
        if conn in self.client_info:
            del self.client_info[conn]

    def _process_key_exchange(self, conn, data):
        """Client'tan gelen key exchange mesajını işler."""
        try:
            info = self.client_info.get(conn)
            if not info:
                return
            
            key_ex = info["key_exchange"]
            
            if key_ex.process_client_key(data):
                info["symmetric_key"] = key_ex.get_symmetric_key()
                info["symmetric_algo"] = key_ex.get_symmetric_algo()
                info["handshake_done"] = True
                
                print(f"[Server] ✅ Key Exchange tamamlandı!")
                print(f"         Algoritma: {info['symmetric_algo']}")
                print(f"         Anahtar: {info['symmetric_key'].hex()}")
                
                # ACK gönder
                ack = json.dumps({
                    "type": "KEY_EXCHANGE_ACK",
                    "status": "success",
                    "algorithm": info["symmetric_algo"]
                })
                conn.sendall(ack.encode())
                
        except Exception as e:
            print(f"[Server] Key exchange hatası: {e}")

    def get_client_symmetric_key(self, conn) -> bytes:
        """Belirli client'ın simetrik anahtarını döndürür."""
        info = self.client_info.get(conn)
        if info:
            return info.get("symmetric_key")
        return None

    def get_client_algo(self, conn) -> str:
        """Belirli client'ın simetrik algoritmasını döndürür."""
        info = self.client_info.get(conn)
        if info:
            return info.get("symmetric_algo")
        return None

    def is_handshake_done(self, conn) -> bool:
        """Key exchange tamamlandı mı?"""
        info = self.client_info.get(conn)
        if info:
            return info.get("handshake_done", False)
        return False

    def send(self, text):
        """Bu fonksiyon Server'dan tüm Client'lara mesaj yollar."""
=======
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
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        for c in self.clients:
            try:
                c.sendall(text.encode())
            except:
<<<<<<< HEAD
                pass

    def send_to(self, conn, text):
        """Belirli bir client'a mesaj gönderir."""
        try:
            conn.sendall(text.encode())
        except:
            pass
=======
                pass
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa

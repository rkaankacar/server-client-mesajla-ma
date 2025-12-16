# -*- coding: utf-8 -*-
"""
Chat Client - RSA Key Exchange destekli
"""

import socket
import threading
import json

from core.encryption.encryption_factory import EncryptionFactory
from core.network.key_exchange import KeyExchangeClient, is_key_exchange_message


class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Key Exchange
        self.key_exchange = KeyExchangeClient()
        self.symmetric_key = None
        self.symmetric_algo = None
        self.handshake_done = False
        self.preferred_algo = "AES"  # Varsayılan: AES
        
        # Callbacks
        self.on_key_exchange_complete = None
        self.on_message_received = None

    def connect(self):
        """Server'a bağlanır."""
        self.client_socket.connect((self.host, self.port))

    def set_preferred_algo(self, algo: str):
        """Tercih edilen simetrik algoritmayı ayarlar (AES veya DES)."""
        if algo in ["AES", "DES"]:
            self.preferred_algo = algo

    def send(self, message):
        """Raw mesaj gönderir."""
        self.client_socket.sendall(message.encode())

    def send_encrypted(self, message, algo_type=None, **kwargs):
        """
        Mesajı şifreler ve gönderir.
        
        Eğer Key Exchange tamamlandıysa, paylaşılan simetrik anahtarı kullanır.
        """
        try:
            # Key exchange sonrası: paylaşılan anahtarı kullan
            if self.handshake_done and self.symmetric_key:
                if algo_type is None or algo_type.startswith(self.symmetric_algo):
                    # Paylaşılan anahtarı kullan
                    if self.symmetric_algo == "AES":
                        from core.encryption.aes_library import AESLibraryCipher
                        cipher = AESLibraryCipher()
                        cipher.key = self.symmetric_key
                    elif self.symmetric_algo == "DES":
                        from core.encryption.des_library import DESLibraryCipher
                        cipher = DESLibraryCipher()
                        cipher.key = self.symmetric_key
                    else:
                        cipher = EncryptionFactory.get_cipher(algo_type, **kwargs)
                else:
                    cipher = EncryptionFactory.get_cipher(algo_type, **kwargs)
            else:
                cipher = EncryptionFactory.get_cipher(algo_type, **kwargs)
            
            encrypted_message = cipher.encrypt(message)
            print(f"[Client] '{message}' -> '{encrypted_message[:50]}...' olarak şifrelenip gönderildi.")
            self.send(encrypted_message)
            
        except Exception as e:
            print(f"Şifreleme hatası: {e}")

    def start_receiving(self, handler):
        """Mesaj alma thread'ini başlatır."""
        self.on_message_received = handler
        threading.Thread(target=self._receive, args=(handler,), daemon=True).start()

    def _receive(self, handler):
        """Mesajları alır ve işler."""
        while True:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    break
                
                # Key Exchange mesajı mı kontrol et
                if is_key_exchange_message(data):
                    self._process_key_exchange(data)
                else:
                    # Normal mesaj
                    handler(data)
                    
            except Exception as e:
                print(f"[Client] Alma hatası: {e}")
                break

    def _process_key_exchange(self, data):
        """Server'dan gelen key exchange mesajlarını işler."""
        try:
            parsed = json.loads(data)
            msg_type = parsed.get("type", "")
            
            if msg_type == "KEY_EXCHANGE_INIT":
                # Server public key gönderdi
                print("[Client] Server public key alındı")
                
                if self.key_exchange.process_server_handshake(data):
                    # Simetrik anahtar oluştur
                    self.key_exchange.generate_symmetric_key(self.preferred_algo)
                    self.symmetric_key = self.key_exchange.get_symmetric_key()
                    self.symmetric_algo = self.key_exchange.get_symmetric_algo()
                    
                    print(f"[Client] {self.symmetric_algo} anahtarı oluşturuldu: {self.symmetric_key.hex()}")
                    
                    # RSA ile şifreli anahtarı gönder
                    response = self.key_exchange.create_key_response()
                    self.send(response)
                    print("[Client] Şifreli anahtar gönderildi")
            
            elif msg_type == "KEY_EXCHANGE_ACK":
                # Server anahtarı aldı ve onayladı
                if parsed.get("status") == "success":
                    self.handshake_done = True
                    print(f"[Client] ✅ Key Exchange tamamlandı! Algoritma: {self.symmetric_algo}")
                    
                    if self.on_key_exchange_complete:
                        self.on_key_exchange_complete(self.symmetric_algo, self.symmetric_key)
                        
        except Exception as e:
            print(f"[Client] Key exchange hatası: {e}")

    def is_handshake_done(self) -> bool:
        """Key exchange tamamlandı mı?"""
        return self.handshake_done

    def get_symmetric_key(self) -> bytes:
        """Paylaşılan simetrik anahtarı döndürür."""
        return self.symmetric_key

    def get_symmetric_algo(self) -> str:
        """Kullanılan simetrik algoritmayı döndürür."""
        return self.symmetric_algo
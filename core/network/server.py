# -*- coding: utf-8 -*-
"""
Chat Server - RSA Key Exchange destekli
Protocol entegreli
"""

import socket
import threading
import json
import os

from core.network.key_exchange import KeyExchangeServer, is_key_exchange_message
from core.network.protocol import Protocol

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.client_info = {}  # {conn: {"addr": addr, "key_exchange": KeyExchangeServer, "symmetric_key": bytes}}
        
        self.plain_messages = []
        self.encrypted_messages = []
        
        # Key Exchange durumu
        self.key_exchange_enabled = True
        self.default_algo = "AES"  # Varsayılan simetrik algoritma
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.port = self.server_socket.getsockname()[1]
        self.server_socket.listen()
        
        if not os.path.exists("server_downloads"):
            os.makedirs("server_downloads")

    def start(self, message_handler):
        threading.Thread(target=self._accept_clients, args=(message_handler,), daemon=True).start()

    def _accept_clients(self, handler):
        while True:
            conn, addr = self.server_socket.accept()
            self.clients.append(conn)
            
            # Her client için key exchange yöneticisi oluştur
            key_ex = KeyExchangeServer(2048)
            self.client_info[conn] = {
                "addr": addr,
                "key_exchange": key_ex,
                "symmetric_key": None,
                "symmetric_algo": None,
                "handshake_done": False,
                "current_file": None
            }
            
            # Key Exchange başlat - public key gönder
            if self.key_exchange_enabled:
                try:
                    handshake = key_ex.create_handshake_message()
                    # Bu başlangıç mesajı eski usul (string) gidebilir ya da Protocol ile
                    # Client tarafı _receive döngüsünde Protocol bekliyorsa, bunu Protocol ile sarmalamalıyız.
                    # ANCAK: Client connect olur olmaz _receive threadini başlatmayabilir.
                    # Yine de standart olması için Protocol ile gönderelim.
                    Protocol.send_packet(conn, Protocol.TYPE_TEXT, handshake)
                    print(f"[Server] Key Exchange başlatıldı: {addr}")
                except Exception as e:
                    print(f"[Server] Handshake hatası: {e}")
            
            threading.Thread(target=self._handle_client, args=(conn, addr, handler), daemon=True).start()

    def _handle_client(self, conn, addr, handler):
        while True:
            try:
                packet_type, payload = Protocol.recv_packet(conn)
                if packet_type is None:
                    break
                
                if packet_type == Protocol.TYPE_TEXT or packet_type == Protocol.TYPE_KEY_EXCHANGE:
                    try:
                        data = payload.decode('utf-8')
                    except:
                        data = payload.decode('latin-1')
                        
                    # Key Exchange mesajı mı kontrol et
                    if is_key_exchange_message(data):
                        self._process_key_exchange(conn, data)
                    else:
                        # Normal şifreli mesaj
                        self.encrypted_messages.append(data)
                        handler(addr, data)
                        # Diğer clientlara ilet (opsiyonel, chat mantığı)
                        # self.broadcast_packet(conn, packet_type, payload)

                elif packet_type == Protocol.TYPE_FILE_METADATA:
                    try:
                        meta_json = payload.decode('utf-8')
                        metadata = json.loads(meta_json)
                        
                        filename = metadata.get("filename", "unknown_file")
                        print(f"[Server] Client'tan dosya geliyor: {filename}")
                        
                        # Server'a kaydetmeye hazırlan
                        self.client_info[conn]["current_file"] = open(os.path.join("server_downloads", filename), "wb")
                        
                        # Diğer clientlara Metadata ilet
                        # self.broadcast_packet(conn, packet_type, payload)
                        
                    except Exception as e:
                        print(f"Server Metadata Hatası: {e}")

                elif packet_type == Protocol.TYPE_FILE_CHUNK:
                    # Dosyayı kaydet
                    f = self.client_info[conn].get("current_file")
                    if f:
                        decrypted_payload = payload
                        # Decrypt attempt
                        try:
                            # Client bilgisinden anahtarı ve algoritmayı al
                            algo = self.client_info[conn].get("symmetric_algo")
                            key = self.client_info[conn].get("symmetric_key")
                            
                            if algo == "AES":
                                algo_factory_name = "AES_Library"
                            elif algo == "DES":
                                algo_factory_name = "DES_Library"
                            else:
                                algo_factory_name = algo
                                
                            if algo_factory_name and key:
                                from core.encryption.encryption_factory import EncryptionFactory
                                cipher = EncryptionFactory.get_cipher(algo_factory_name, key=key)
                                
                                if hasattr(cipher, 'decrypt_bytes'):
                                     decrypted_payload = cipher.decrypt_bytes(payload)
                                else:
                                    # Fallback (Eğer text algosu seçildiyse)
                                    pass
                        except Exception as e:
                            print(f"Decryption error on file chunk: {e}")
                            # Hata olsa bile yazmayı dener veya loglar
                        
                        f.write(decrypted_payload)
                        f.close()
                        self.client_info[conn]["current_file"] = None
                        print("[Server] Dosya server'a kaydedildi.")
                        handler(addr, f"[DOSYA GÖNDERDİ]: {len(decrypted_payload)} bytes")
                    
                    # Diğer clientlara ilet
                    # self.broadcast_packet(conn, packet_type, payload)

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
                # Key Exchange mesajları Protocol.TYPE_KEY_EXCHANGE veya TYPE_TEXT ile gidebilir
                Protocol.send_packet(conn, Protocol.TYPE_KEY_EXCHANGE, ack)
                
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
        """Bu fonksiyon Server'dan tüm Client'lara mesaj yollar (Broadcast)."""
        # Text mesajlarını şifreli varsayıyoruz (UI şifreleyip veriyor)
        for c in self.clients:
            try:
                Protocol.send_packet(c, Protocol.TYPE_TEXT, text)
            except:
                pass

    def send_to(self, conn, text):
        """Belirli bir client'a mesaj gönderir."""
        try:
             Protocol.send_packet(conn, Protocol.TYPE_TEXT, text)
        except:
            pass
            
    def broadcast_packet(self, sender_conn, packet_type, payload):
        """Packet'i gönderen hariç herkese ilet."""
        for c in self.clients:
            if c != sender_conn:
                try:
                    Protocol.send_packet(c, packet_type, payload)
                except:
                    pass

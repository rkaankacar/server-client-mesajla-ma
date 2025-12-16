# -*- coding: utf-8 -*-
"""
RSA Key Exchange Protocol
Server ve Client arasında güvenli simetrik anahtar paylaşımı
"""

import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


class KeyExchangeServer:
    """
    Server tarafı Key Exchange yöneticisi.
    
    Akış:
    1. RSA key pair oluştur
    2. Public key'i client'a gönder
    3. Client'ın şifrelenmiş simetrik anahtarını al
    4. Private key ile çöz
    """
    
    def __init__(self, key_size: int = 2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        self.symmetric_key = None
        self.symmetric_algo = None  # "AES" veya "DES"
        self._generate_rsa_keys()
    
    def _generate_rsa_keys(self):
        """RSA key pair oluşturur."""
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()
    
    def get_public_key_pem(self) -> str:
        """Public key'i PEM formatında döndürür."""
        return self.public_key.export_key().decode('utf-8')
    
    def create_handshake_message(self) -> str:
        """
        Client'a gönderilecek handshake mesajını oluşturur.
        JSON formatında: {"type": "KEY_EXCHANGE", "public_key": "..."}
        """
        message = {
            "type": "KEY_EXCHANGE_INIT",
            "public_key": self.get_public_key_pem()
        }
        return json.dumps(message)
    
    def process_client_key(self, encrypted_data: str) -> bool:
        """
        Client'tan gelen şifrelenmiş simetrik anahtarı çözer.
        
        Args:
            encrypted_data: JSON formatında şifrelenmiş anahtar verisi
            
        Returns:
            True eğer başarılı, False değilse
        """
        try:
            data = json.loads(encrypted_data)
            
            if data.get("type") != "KEY_EXCHANGE_RESPONSE":
                return False
            
            # RSA ile şifrelenmiş anahtarı çöz
            cipher = PKCS1_OAEP.new(self.private_key)
            encrypted_key = base64.b64decode(data["encrypted_key"])
            self.symmetric_key = cipher.decrypt(encrypted_key)
            self.symmetric_algo = data.get("algorithm", "AES")
            
            return True
            
        except Exception as e:
            print(f"Key exchange hatası: {e}")
            return False
    
    def get_symmetric_key(self) -> bytes:
        """Çözülmüş simetrik anahtarı döndürür."""
        return self.symmetric_key
    
    def get_symmetric_algo(self) -> str:
        """Simetrik algoritma adını döndürür."""
        return self.symmetric_algo


class KeyExchangeClient:
    """
    Client tarafı Key Exchange yöneticisi.
    
    Akış:
    1. Server'ın public key'ini al
    2. Simetrik anahtar oluştur (AES veya DES)
    3. Public key ile şifrele
    4. Server'a gönder
    """
    
    def __init__(self):
        self.server_public_key = None
        self.symmetric_key = None
        self.symmetric_algo = None
    
    def process_server_handshake(self, handshake_data: str) -> bool:
        """
        Server'dan gelen handshake mesajını işler.
        
        Args:
            handshake_data: JSON formatında handshake verisi
            
        Returns:
            True eğer başarılı
        """
        try:
            data = json.loads(handshake_data)
            
            if data.get("type") != "KEY_EXCHANGE_INIT":
                return False
            
            # Server'ın public key'ini yükle
            self.server_public_key = RSA.import_key(data["public_key"])
            return True
            
        except Exception as e:
            print(f"Handshake hatası: {e}")
            return False
    
    def generate_symmetric_key(self, algorithm: str = "AES") -> bytes:
        """
        Simetrik anahtar oluşturur.
        
        Args:
            algorithm: "AES" (16 byte) veya "DES" (8 byte)
        """
        self.symmetric_algo = algorithm
        
        if algorithm == "AES":
            self.symmetric_key = get_random_bytes(16)  # AES-128
        elif algorithm == "DES":
            self.symmetric_key = get_random_bytes(8)   # DES
        else:
            raise ValueError(f"Desteklenmeyen algoritma: {algorithm}")
        
        return self.symmetric_key
    
    def create_key_response(self) -> str:
        """
        Server'a gönderilecek şifreli anahtar mesajını oluşturur.
        """
        if self.server_public_key is None:
            raise Exception("Server public key yok!")
        
        if self.symmetric_key is None:
            raise Exception("Simetrik anahtar oluşturulmadı!")
        
        # RSA ile simetrik anahtarı şifrele
        cipher = PKCS1_OAEP.new(self.server_public_key)
        encrypted_key = cipher.encrypt(self.symmetric_key)
        
        message = {
            "type": "KEY_EXCHANGE_RESPONSE",
            "algorithm": self.symmetric_algo,
            "encrypted_key": base64.b64encode(encrypted_key).decode('utf-8')
        }
        return json.dumps(message)
    
    def get_symmetric_key(self) -> bytes:
        """Oluşturulan simetrik anahtarı döndürür."""
        return self.symmetric_key
    
    def get_symmetric_algo(self) -> str:
        """Simetrik algoritma adını döndürür."""
        return self.symmetric_algo


def is_key_exchange_message(data: str) -> bool:
    """Mesajın key exchange mesajı olup olmadığını kontrol eder."""
    try:
        parsed = json.loads(data)
        return parsed.get("type", "").startswith("KEY_EXCHANGE")
    except:
        return False


# Test
if __name__ == "__main__":
    print("=== RSA Key Exchange Test ===\n")
    
    # 1. Server key pair oluşturur
    server = KeyExchangeServer(2048)
    print("✅ Server RSA key pair oluşturuldu")
    
    # 2. Server handshake mesajı oluşturur
    handshake = server.create_handshake_message()
    print(f"📤 Server handshake gönderdi (public key)")
    
    # 3. Client handshake'i alır
    client = KeyExchangeClient()
    client.process_server_handshake(handshake)
    print("✅ Client server public key'i aldı")
    
    # 4. Client AES anahtarı oluşturur
    client.generate_symmetric_key("AES")
    print(f"🔑 Client AES anahtarı oluşturdu: {client.get_symmetric_key().hex()}")
    
    # 5. Client anahtarı RSA ile şifreler
    response = client.create_key_response()
    print("📤 Client şifreli anahtarı gönderdi")
    
    # 6. Server anahtarı çözer
    server.process_client_key(response)
    print(f"🔓 Server anahtarı çözdü: {server.get_symmetric_key().hex()}")
    
    # 7. Doğrulama
    match = client.get_symmetric_key() == server.get_symmetric_key()
    print(f"\n{'✅' if match else '❌'} Anahtarlar eşleşiyor: {match}")

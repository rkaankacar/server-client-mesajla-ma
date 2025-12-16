# -*- coding: utf-8 -*-
"""
RSA Library Implementation
Kütüphane tabanlı RSA implementasyonu (pycryptodome)
Hem veri şifreleme hem de anahtar dağıtımı için kullanılabilir.
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64


class RSALibraryCipher:
    """
    RSA-2048 kullanan kütüphane tabanlı şifreleme sınıfı.
    - Anahtar: 2048 bit
    - Padding: OAEP
    - Kullanım: Simetrik anahtar dağıtımı (Key Exchange)
    """
    
    def __init__(self, key_size: int = 2048):
        """
        Args:
            key_size: RSA anahtar boyutu (varsayılan 2048 bit)
        """
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        self._generate_key_pair()
    
    def _generate_key_pair(self):
        """RSA key pair oluşturur."""
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()
    
    def get_public_key_pem(self) -> str:
        """Public key'i PEM formatında döndürür."""
        return self.public_key.export_key().decode('utf-8')
    
    def get_private_key_pem(self) -> str:
        """Private key'i PEM formatında döndürür."""
        return self.private_key.export_key().decode('utf-8')
    
    def set_public_key_from_pem(self, pem_data: str):
        """PEM formatından public key yükler."""
        self.public_key = RSA.import_key(pem_data)
    
    def set_private_key_from_pem(self, pem_data: str):
        """PEM formatından private key yükler."""
        self.private_key = RSA.import_key(pem_data)
        self.public_key = self.private_key.publickey()
    
    def encrypt(self, plaintext: str) -> str:
        """
        Metni RSA-OAEP ile şifreler (public key kullanarak).
        
        NOT: RSA ile doğrudan veri şifreleme önerilmez.
        Genellikle simetrik anahtar şifrelemek için kullanılır.
        
        Args:
            plaintext: Şifrelenecek metin (max ~190 byte for RSA-2048)
            
        Returns:
            Base64 kodlanmış şifreli metin
        """
        if not plaintext:
            return ""
        
        try:
            cipher = PKCS1_OAEP.new(self.public_key)
            plaintext_bytes = plaintext.encode('utf-8')
            
            # RSA-2048 OAEP ile max ~190 byte şifrelenebilir
            # Uzun metinler için chunk'lara bölmek gerekir
            max_chunk = (self.key_size // 8) - 42  # OAEP overhead
            
            if len(plaintext_bytes) <= max_chunk:
                ciphertext = cipher.encrypt(plaintext_bytes)
                return base64.b64encode(ciphertext).decode('utf-8')
            else:
                # Uzun metin - chunk'lara böl
                chunks = []
                for i in range(0, len(plaintext_bytes), max_chunk):
                    chunk = plaintext_bytes[i:i+max_chunk]
                    encrypted_chunk = cipher.encrypt(chunk)
                    chunks.append(base64.b64encode(encrypted_chunk).decode('utf-8'))
                return '|'.join(chunks)
                
        except Exception as e:
            return f"RSA Şifreleme Hatası: {e}"
    
    def decrypt(self, ciphertext: str) -> str:
        """
        RSA-OAEP ile şifrelenmiş metni çözer (private key kullanarak).
        
        Args:
            ciphertext: Base64 kodlanmış şifreli metin
            
        Returns:
            Çözülmüş düz metin
        """
        if not ciphertext:
            return ""
        
        try:
            cipher = PKCS1_OAEP.new(self.private_key)
            
            if '|' in ciphertext:
                # Chunked ciphertext
                plaintext_parts = []
                for chunk in ciphertext.split('|'):
                    encrypted_chunk = base64.b64decode(chunk)
                    decrypted_chunk = cipher.decrypt(encrypted_chunk)
                    plaintext_parts.append(decrypted_chunk)
                return b''.join(plaintext_parts).decode('utf-8')
            else:
                encrypted_data = base64.b64decode(ciphertext)
                plaintext = cipher.decrypt(encrypted_data)
                return plaintext.decode('utf-8')
                
        except Exception as e:
            return f"RSA Çözme Hatası: {e}"
    
    def encrypt_symmetric_key(self, key_bytes: bytes) -> str:
        """
        Simetrik anahtarı RSA ile şifreler (Key Exchange için).
        
        Args:
            key_bytes: Şifrelenecek simetrik anahtar (bytes)
            
        Returns:
            Base64 kodlanmış şifrelenmiş anahtar
        """
        try:
            cipher = PKCS1_OAEP.new(self.public_key)
            encrypted_key = cipher.encrypt(key_bytes)
            return base64.b64encode(encrypted_key).decode('utf-8')
        except Exception as e:
            raise Exception(f"Simetrik anahtar şifreleme hatası: {e}")
    
    def decrypt_symmetric_key(self, encrypted_key: str) -> bytes:
        """
        RSA ile şifrelenmiş simetrik anahtarı çözer.
        
        Args:
            encrypted_key: Base64 kodlanmış şifreli anahtar
            
        Returns:
            Çözülmüş simetrik anahtar (bytes)
        """
        try:
            cipher = PKCS1_OAEP.new(self.private_key)
            encrypted_data = base64.b64decode(encrypted_key)
            return cipher.decrypt(encrypted_data)
        except Exception as e:
            raise Exception(f"Simetrik anahtar çözme hatası: {e}")
    
    def save_keys(self, public_path: str, private_path: str):
        """Anahtarları dosyaya kaydeder."""
        with open(public_path, 'w') as f:
            f.write(self.get_public_key_pem())
        with open(private_path, 'w') as f:
            f.write(self.get_private_key_pem())
    
    def load_keys(self, public_path: str = None, private_path: str = None):
        """Anahtarları dosyadan yükler."""
        if public_path:
            with open(public_path, 'r') as f:
                self.set_public_key_from_pem(f.read())
        if private_path:
            with open(private_path, 'r') as f:
                self.set_private_key_from_pem(f.read())


# Test
if __name__ == "__main__":
    # RSA cipher oluştur
    cipher = RSALibraryCipher(2048)
    
    # Kısa metin testi
    original = "Merhaba, bu RSA testi!"
    encrypted = cipher.encrypt(original)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Orijinal: {original}")
    print(f"Şifreli: {encrypted[:50]}...")
    print(f"Çözülmüş: {decrypted}")
    
    # Simetrik anahtar exchange testi
    aes_key = get_random_bytes(16)
    print(f"\nAES Key (hex): {aes_key.hex()}")
    
    encrypted_aes = cipher.encrypt_symmetric_key(aes_key)
    print(f"Şifreli AES Key: {encrypted_aes[:50]}...")
    
    decrypted_aes = cipher.decrypt_symmetric_key(encrypted_aes)
    print(f"Çözülen AES Key (hex): {decrypted_aes.hex()}")
    print(f"Eşleşme: {aes_key == decrypted_aes}")

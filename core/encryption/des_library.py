# -*- coding: utf-8 -*-
"""
DES Library Implementation
Kütüphane tabanlı DES-CBC implementasyonu (pycryptodome)
"""

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


class DESLibraryCipher:
    """
    DES-CBC modu kullanan kütüphane tabanlı şifreleme sınıfı.
    - Anahtar: 8 byte (64 bit, 56 bit efektif)
    - IV: 8 byte
    - Padding: PKCS7
    """
    
    def __init__(self, key = None):
        """
        Args:
            key: 8 byte (bytes) veya 8 karakter (str). Belirtilmezse rastgele üretilir.
        """
        if key is None:
            self.key = get_random_bytes(8)
        else:
            if isinstance(key, str):
                key_bytes = key.encode('utf-8')
            else:
                key_bytes = key

            # Key'i 8 byte'a ayarla
            if len(key_bytes) < 8:
                key_bytes = key_bytes.ljust(8, b'\0')
            elif len(key_bytes) > 8:
                key_bytes = key_bytes[:8]
            self.key = key_bytes
    
    def encrypt(self, plaintext: str) -> str:
        """
        Metni DES-CBC ile şifreler.
        
        Args:
            plaintext: Şifrelenecek düz metin
            
        Returns:
            Base64 kodlanmış şifreli metin (IV + ciphertext)
        """
        if not plaintext:
            return ""
        
        try:
            # Rastgele IV oluştur
            iv = get_random_bytes(8)
            
            # Cipher oluştur
            cipher = DES.new(self.key, DES.MODE_CBC, iv)
            
            # Metni byte'a çevir ve padding uygula
            plaintext_bytes = plaintext.encode('utf-8')
            padded_data = pad(plaintext_bytes, DES.block_size)
            
            # Şifrele
            ciphertext = cipher.encrypt(padded_data)
            
            # IV + ciphertext birleştir ve base64 kodla
            encrypted = base64.b64encode(iv + ciphertext).decode('utf-8')
            return encrypted
            
        except Exception as e:
            return f"DES Şifreleme Hatası: {e}"
    
    def decrypt(self, ciphertext: str) -> str:
        """
        DES-CBC ile şifrelenmiş metni çözer.
        
        Args:
            ciphertext: Base64 kodlanmış şifreli metin (IV + ciphertext)
            
        Returns:
            Çözülmüş düz metin
        """
        if not ciphertext:
            return ""
        
        try:
            # Base64 decode
            encrypted_data = base64.b64decode(ciphertext)
            
            # IV ve ciphertext'i ayır
            iv = encrypted_data[:8]
            actual_ciphertext = encrypted_data[8:]
            
            # Cipher oluştur
            cipher = DES.new(self.key, DES.MODE_CBC, iv)
            
            # Çöz ve unpad
            decrypted_padded = cipher.decrypt(actual_ciphertext)
            plaintext = unpad(decrypted_padded, DES.block_size)
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            return f"DES Çözme Hatası: {e}"
    
    def get_key_hex(self) -> str:
        """Anahtarı hex formatında döndürür."""
        return self.key.hex()
    
    def get_key_base64(self) -> str:
        """Anahtarı base64 formatında döndürür."""
        return base64.b64encode(self.key).decode('utf-8')

    def encrypt_bytes(self, data: bytes) -> bytes:
        """
        Byte verisini DES-CBC ile şifreler (Raw).
        
        Args:
            data: Şifrelenecek byte verisi
            
        Returns:
            IV (8 bytes) + Encrypted Data (bytes)
        """
        if not data:
            return b""
        
        try:
            # Rastgele IV oluştur
            iv = get_random_bytes(8)
            
            # Cipher oluştur
            cipher = DES.new(self.key, DES.MODE_CBC, iv)
            
            # Padding uygula
            padded_data = pad(data, DES.block_size)
            
            # Şifrele
            ciphertext = cipher.encrypt(padded_data)
            
            # IV + ciphertext birleştir
            return iv + ciphertext
            
        except Exception as e:
            print(f"DES Byte Şifreleme Hatası: {e}")
            return b""

    def decrypt_bytes(self, encrypted_data: bytes) -> bytes:
        """
        DES-CBC ile şifrelenmiş byte verisini çözer (Raw).
        
        Args:
            encrypted_data: IV (8 bytes) + Encrypted Data (bytes)
            
        Returns:
            Çözülmüş byte verisi
        """
        if not encrypted_data or len(encrypted_data) < 8:
            return b""
        
        try:
            # IV ve ciphertext'i ayır
            iv = encrypted_data[:8]
            actual_ciphertext = encrypted_data[8:]
            
            # Cipher oluştur
            cipher = DES.new(self.key, DES.MODE_CBC, iv)
            
            # Çöz ve unpad
            decrypted_padded = cipher.decrypt(actual_ciphertext)
            plaintext = unpad(decrypted_padded, DES.block_size)
            
            return plaintext
            
        except Exception as e:
            print(f"DES Byte Çözme Hatası: {e}")
            return b""


# Test
if __name__ == "__main__":
    # Sabit key ile test
    cipher = DESLibraryCipher("MyKey123")
    
    original = "Merhaba, bu bir DES testi!"
    encrypted = cipher.encrypt(original)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Orijinal: {original}")
    print(f"Şifreli: {encrypted}")
    print(f"Çözülmüş: {decrypted}")
    print(f"Anahtar (hex): {cipher.get_key_hex()}")

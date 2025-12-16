# -*- coding: utf-8 -*-
"""
Key Manager
Anahtar üretimi, kaydetme ve yükleme işlemleri
"""

import os
import secrets
import base64


class KeyManager:
    """
    Kriptografik anahtar yönetimi sınıfı.
    - AES anahtarı: 16 byte (128 bit)
    - DES anahtarı: 8 byte (64 bit)
    - RSA: pycryptodome ile ayrı yönetilir
    """
    
    def __init__(self, keys_dir: str = None):
        """
        Args:
            keys_dir: Anahtarların saklanacağı klasör yolu
        """
        if keys_dir is None:
            # Proje kök dizininde keys klasörü
            self.keys_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "keys"
            )
        else:
            self.keys_dir = keys_dir
        
        # Klasör yoksa oluştur
        os.makedirs(self.keys_dir, exist_ok=True)
    
    # ============== AES Anahtar Yönetimi ==============
    
    def generate_aes_key(self) -> bytes:
        """16 byte rastgele AES-128 anahtarı üretir."""
        return secrets.token_bytes(16)
    
    def save_aes_key(self, key: bytes, filename: str = "aes_key.bin"):
        """AES anahtarını binary dosyaya kaydeder."""
        filepath = os.path.join(self.keys_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(key)
        return filepath
    
    def load_aes_key(self, filename: str = "aes_key.bin") -> bytes:
        """AES anahtarını dosyadan yükler."""
        filepath = os.path.join(self.keys_dir, filename)
        if not os.path.exists(filepath):
            # Dosya yoksa yeni anahtar üret ve kaydet
            key = self.generate_aes_key()
            self.save_aes_key(key, filename)
            return key
        with open(filepath, 'rb') as f:
            return f.read()
    
    def get_or_create_aes_key(self, filename: str = "aes_key.bin") -> bytes:
        """AES anahtarını yükler, yoksa oluşturur."""
        return self.load_aes_key(filename)
    
    # ============== DES Anahtar Yönetimi ==============
    
    def generate_des_key(self) -> bytes:
        """8 byte rastgele DES anahtarı üretir."""
        return secrets.token_bytes(8)
    
    def save_des_key(self, key: bytes, filename: str = "des_key.bin"):
        """DES anahtarını binary dosyaya kaydeder."""
        filepath = os.path.join(self.keys_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(key)
        return filepath
    
    def load_des_key(self, filename: str = "des_key.bin") -> bytes:
        """DES anahtarını dosyadan yükler."""
        filepath = os.path.join(self.keys_dir, filename)
        if not os.path.exists(filepath):
            # Dosya yoksa yeni anahtar üret ve kaydet
            key = self.generate_des_key()
            self.save_des_key(key, filename)
            return key
        with open(filepath, 'rb') as f:
            return f.read()
    
    def get_or_create_des_key(self, filename: str = "des_key.bin") -> bytes:
        """DES anahtarını yükler, yoksa oluşturur."""
        return self.load_des_key(filename)
    
    # ============== Utility Fonksiyonlar ==============
    
    @staticmethod
    def key_to_hex(key: bytes) -> str:
        """Anahtarı hex string'e çevirir."""
        return key.hex()
    
    @staticmethod
    def hex_to_key(hex_str: str) -> bytes:
        """Hex string'i byte anahtara çevirir."""
        return bytes.fromhex(hex_str)
    
    @staticmethod
    def key_to_base64(key: bytes) -> str:
        """Anahtarı base64 string'e çevirir."""
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def base64_to_key(b64_str: str) -> bytes:
        """Base64 string'i byte anahtara çevirir."""
        return base64.b64decode(b64_str)
    
    @staticmethod
    def string_to_aes_key(key_str: str) -> bytes:
        """String'i 16 byte AES anahtarına dönüştürür."""
        key_bytes = key_str.encode('utf-8')
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\0')
        elif len(key_bytes) > 16:
            key_bytes = key_bytes[:16]
        return key_bytes
    
    @staticmethod
    def string_to_des_key(key_str: str) -> bytes:
        """String'i 8 byte DES anahtarına dönüştürür."""
        key_bytes = key_str.encode('utf-8')
        if len(key_bytes) < 8:
            key_bytes = key_bytes.ljust(8, b'\0')
        elif len(key_bytes) > 8:
            key_bytes = key_bytes[:8]
        return key_bytes
    
    def list_keys(self) -> list:
        """Kayıtlı anahtar dosyalarını listeler."""
        keys = []
        if os.path.exists(self.keys_dir):
            for f in os.listdir(self.keys_dir):
                filepath = os.path.join(self.keys_dir, f)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    keys.append({
                        "filename": f,
                        "path": filepath,
                        "size_bytes": size
                    })
        return keys
    
    def delete_key(self, filename: str) -> bool:
        """Anahtar dosyasını siler."""
        filepath = os.path.join(self.keys_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False


# Test
if __name__ == "__main__":
    km = KeyManager()
    
    # AES key test
    aes_key = km.generate_aes_key()
    print(f"AES Key (hex): {km.key_to_hex(aes_key)}")
    print(f"AES Key (base64): {km.key_to_base64(aes_key)}")
    km.save_aes_key(aes_key)
    
    # DES key test
    des_key = km.generate_des_key()
    print(f"DES Key (hex): {km.key_to_hex(des_key)}")
    km.save_des_key(des_key)
    
    # Kayıtlı anahtarları listele
    print("\nKayıtlı anahtarlar:")
    for k in km.list_keys():
        print(f"  - {k['filename']} ({k['size_bytes']} bytes)")

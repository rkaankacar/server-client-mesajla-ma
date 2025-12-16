<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Encryption Factory - Güncellenmiş Versiyon
Tüm şifreleme algoritmalarını merkezi olarak yöneten factory sınıfı.
Kütüphane tabanlı ve manuel implementasyonları destekler.
"""

# Klasik şifreler
=======
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
from core.encryption.caesar import CaesarCipher
from core.encryption.vigenere import VigenereCipher
from core.encryption.substitution import SubstitutionCipher
from core.encryption.affine import AffineCipher
from core.encryption.rail_fence import RailFenceCipher
from core.encryption.playfair import PlayfairCipher
from core.encryption.rot13 import Rot13Cipher
from core.encryption.columnar import ColumnarCipher
from core.encryption.polybius import PolybiusCipher
from core.encryption.pigpen import PigpenCipher
from core.encryption.route import RouteCipher
from core.encryption.hill import HillCipher
<<<<<<< HEAD

# Eski implementasyonlar (geriye uyumluluk için)
=======
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
from core.encryption.rsa import RSACipher
from core.encryption.des import DESCipher
from core.encryption.dsa import DSACipher

<<<<<<< HEAD
# Yeni modern kriptografi - Library tabanlı
from core.encryption.aes_library import AESLibraryCipher
from core.encryption.des_library import DESLibraryCipher
from core.encryption.rsa_library import RSALibraryCipher

# Manuel implementasyonlar
from core.encryption.aes_manual import AESManualCipher


class EncryptionFactory:
    """
    Şifreleme algoritmalarını oluşturan factory sınıfı.
    
    Desteklenen Algoritmalar:
    -------------------------
    Klasik Şifreler:
        - Sezar, Vigenere, Substitution, Affine, RailFence
        - Playfair, ROT13, Columnar, Polybius, Pigpen
        - Route, Hill
    
    Modern Şifreler (Kütüphane Tabanlı):
        - AES_Library: pycryptodome ile AES-128-CBC
        - DES_Library: pycryptodome ile DES-CBC
        - RSA_Library: pycryptodome ile RSA-2048 OAEP
    
    Manuel İmplementasyonlar:
        - AES_Manual: Sıfırdan kodlanmış AES-128-ECB
        - DES: Basitleştirilmiş Feistel yapısı (mevcut)
        - RSA: Temel modüler aritmetik (mevcut)
    """
    
    # Algoritma kategorileri
    CLASSIC_ALGORITHMS = [
        "Sezar", "Vigenere", "Substitution", "Affine", "RailFence",
        "Playfair", "ROT13", "Columnar", "Polybius", "Pigpen",
        "Route", "Hill"
    ]
    
    LIBRARY_ALGORITHMS = [
        "AES_Library", "DES_Library", "RSA_Library"
    ]
    
    MANUAL_ALGORITHMS = [
        "AES_Manual", "DES", "RSA", "DSA"
    ]
    
    ALL_ALGORITHMS = CLASSIC_ALGORITHMS + LIBRARY_ALGORITHMS + MANUAL_ALGORITHMS
    
    @staticmethod
    def get_cipher(algo: str, **kwargs):
        """
        Seçilen algoritmaya göre cipher nesnesi döndürür.
        
        Args:
            algo: Algoritma adı
            **kwargs: Algoritmaya özel parametreler
                - shift: Caesar için kayma miktarı
                - key: Anahtar (Vigenere, AES, DES vb.)
                - a, b: Affine parametreleri
                - rails: RailFence/Route için satır sayısı
        
        Returns:
            Cipher nesnesi (encrypt/decrypt metodları olan)
        """
        
        # ============ KLASİK ŞİFRELER ============
        if algo == "Sezar":
            return CaesarCipher(kwargs.get("shift", 3))
        
        elif algo == "Vigenere":
            return VigenereCipher(kwargs.get("key", "KEY"))
        
        elif algo == "Substitution":
            return SubstitutionCipher()
        
        elif algo == "Affine":
            return AffineCipher(kwargs.get("a", 5), kwargs.get("b", 8))
        
        elif algo == "RailFence":
            return RailFenceCipher(kwargs.get("rails", 3))
        
        elif algo == "Playfair":
            return PlayfairCipher(kwargs.get("key", "KEY"))
        
        elif algo == "ROT13":
            return Rot13Cipher()
        
        elif algo == "Columnar":
            return ColumnarCipher(kwargs.get("key", "KEY"))
        
        elif algo == "Polybius":
            return PolybiusCipher(kwargs.get("key", ""))
        
        elif algo == "Pigpen":
            return PigpenCipher()
        
        elif algo == "Route":
            return RouteCipher(kwargs.get("rails", 4))
        
        elif algo == "Hill":
            return HillCipher(kwargs.get("key", "HILL"))
        
        # ============ KÜTÜPHANE TABANLI MODERN ŞİFRELER ============
        elif algo == "AES_Library":
            return AESLibraryCipher(kwargs.get("key", None))
        
        elif algo == "DES_Library":
            return DESLibraryCipher(kwargs.get("key", None))
        
        elif algo == "RSA_Library":
            return RSALibraryCipher(kwargs.get("key_size", 2048))
        
        # ============ MANUEL İMPLEMENTASYONLAR ============
        elif algo == "AES_Manual":
            return AESManualCipher(kwargs.get("key", None))
        
        elif algo == "DES":
            return DESCipher(kwargs.get("key", "KEY"))
        
        elif algo == "RSA":
            return RSACipher()
        
        elif algo == "DSA":
            return DSACipher()
        
        else:
            raise ValueError(f"Geçersiz algoritma seçimi: {algo}")
    
    @staticmethod
    def get_algorithm_info(algo: str) -> dict:
        """
        Algoritma hakkında bilgi döndürür.
        
        Returns:
            dict: {
                "name": str,
                "type": "classic" | "library" | "manual",
                "key_size": int (bytes) or None,
                "description": str
            }
        """
        info = {
            # Klasik
            "Sezar": {"type": "classic", "key_size": None, "description": "Karakterleri sabit sayı kadar kaydırır"},
            "Vigenere": {"type": "classic", "key_size": None, "description": "Anahtar kelime ile polialfabetik şifreleme"},
            "Substitution": {"type": "classic", "key_size": None, "description": "Harf değiştirme şifresi"},
            "Affine": {"type": "classic", "key_size": None, "description": "ax + b mod 26 formülü"},
            "RailFence": {"type": "classic", "key_size": None, "description": "Zikzak desenli transpozisyon"},
            "Playfair": {"type": "classic", "key_size": None, "description": "5x5 matris ile digraf şifreleme"},
            "ROT13": {"type": "classic", "key_size": None, "description": "13 kaydırmalı Caesar"},
            "Columnar": {"type": "classic", "key_size": None, "description": "Sütunlara göre transpozisyon"},
            "Polybius": {"type": "classic", "key_size": None, "description": "5x5 kare şifresi"},
            "Pigpen": {"type": "classic", "key_size": None, "description": "Masonik şifre"},
            "Route": {"type": "classic", "key_size": None, "description": "Matris yolu şifresi"},
            "Hill": {"type": "classic", "key_size": None, "description": "Matris çarpımı ile şifreleme"},
            
            # Kütüphane tabanlı
            "AES_Library": {"type": "library", "key_size": 16, "description": "AES-128-CBC (pycryptodome)"},
            "DES_Library": {"type": "library", "key_size": 8, "description": "DES-CBC (pycryptodome)"},
            "RSA_Library": {"type": "library", "key_size": 256, "description": "RSA-2048 OAEP (pycryptodome)"},
            
            # Manuel
            "AES_Manual": {"type": "manual", "key_size": 16, "description": "Manuel AES-128-ECB (S-box, rounds)"},
            "DES": {"type": "manual", "key_size": 8, "description": "Basitleştirilmiş DES (Feistel)"},
            "RSA": {"type": "manual", "key_size": None, "description": "Temel RSA (modüler aritmetik)"},
            "DSA": {"type": "manual", "key_size": None, "description": "Digital Signature Algorithm"},
        }
        
        if algo in info:
            result = info[algo].copy()
            result["name"] = algo
            return result
        return None
    
    @staticmethod
    def get_algorithms_by_type(algo_type: str) -> list:
        """
        Belirli tipteki algoritmaları listeler.
        
        Args:
            algo_type: "classic", "library", veya "manual"
        """
        if algo_type == "classic":
            return EncryptionFactory.CLASSIC_ALGORITHMS.copy()
        elif algo_type == "library":
            return EncryptionFactory.LIBRARY_ALGORITHMS.copy()
        elif algo_type == "manual":
            return EncryptionFactory.MANUAL_ALGORITHMS.copy()
        else:
            return EncryptionFactory.ALL_ALGORITHMS.copy()
=======
class EncryptionFactory:
    @staticmethod
    def get_cipher(algo: str, **kwargs):
        if algo == "Sezar":
            return CaesarCipher(kwargs.get("shift", 3))
        elif algo == "Vigenere":
            return VigenereCipher(kwargs.get("key", "KEY"))
        elif algo == "Substitution":
            return SubstitutionCipher()
        elif algo == "Affine":
            return AffineCipher(kwargs.get("a", 5), kwargs.get("b", 8))
        elif algo == "RailFence":
            return RailFenceCipher(kwargs.get("rails", 3))
        elif algo == "Playfair":
            return PlayfairCipher(kwargs.get("key", "KEY"))
        elif algo == "ROT13":
            return Rot13Cipher()
        elif algo == "Columnar":
            return ColumnarCipher(kwargs.get("key", "KEY"))
        elif algo == "Polybius":
            return PolybiusCipher(kwargs.get("key", ""))
        elif algo == "Pigpen":
            return PigpenCipher()
        elif algo == "Route":
            return RouteCipher(kwargs.get("rails", 4))
        elif algo == "Hill":
            return HillCipher(kwargs.get("key", "HILL"))
        elif algo == "RSA":
            return RSACipher()
        elif algo == "DES":
            return DESCipher(kwargs.get("key", "KEY"))
        elif algo == "DSA":
            return DSACipher()
        else:
            raise ValueError("Geçersiz algoritma seçimi.")
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa

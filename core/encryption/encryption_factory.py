from core.encryption.caesar import CaesarCipher
from core.encryption.vigenere import VigenereCipher
from core.encryption.substitution import SubstitutionCipher
from core.encryption.affine import AffineCipher

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
        else:
            raise ValueError("Geçersiz algoritma seçimi.")

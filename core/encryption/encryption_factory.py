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
from core.encryption.rsa import RSACipher
from core.encryption.des import DESCipher
from core.encryption.dsa import DSACipher

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

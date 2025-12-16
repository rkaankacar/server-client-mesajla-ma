import string
import random

class SubstitutionCipher:
    ALPHABET_LOWER = string.ascii_lowercase
    ALPHABET_UPPER = string.ascii_uppercase

    def __init__(self, key: str = "DEFAULT_SEED"):
     
        letters = list(self.ALPHABET_LOWER)
        
       
        random.seed(key)
        
        shuffled = letters[:]
        random.shuffle(shuffled)
        
        # Karışık harita oluştur (a -> x, b -> m gibi)
        self.key_map = {p: c for p, c in zip(letters, shuffled)}
        self.inverse_key_map = {v: k for k, v in self.key_map.items()}

    def encrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                res += self.key_map.get(c, c)
            elif c.isupper():
                lower = c.lower()
                res += self.key_map.get(lower, lower).upper()
            else:
                res += c
        return res

    def decrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                res += self.inverse_key_map.get(c, c)
            elif c.isupper():
                lower = c.lower()
                res += self.inverse_key_map.get(lower, lower).upper()
            else:
                res += c
        return res
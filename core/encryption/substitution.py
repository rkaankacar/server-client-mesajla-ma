import string
import random

class SubstitutionCipher:
    ALPHABET_LOWER = string.ascii_lowercase
    ALPHABET_UPPER = string.ascii_uppercase

    def __init__(self, key: dict = None):
        letters = list(self.ALPHABET_LOWER)
        if key is None:
            shuffled = letters[:]
            random.shuffle(shuffled)
            self.key = {p: c for p, c in zip(letters, shuffled)}
        else:
            self.key = key
        self.inverse_key = {v: k for k, v in self.key.items()}

    def encrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                res += self.key.get(c, c)
            elif c.isupper():
                lower = c.lower()
                res += self.key.get(lower, lower).upper()
            else:
                res += c
        return res

    def decrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                res += self.inverse_key.get(c, c)
            elif c.isupper():
                lower = c.lower()
                res += self.inverse_key.get(lower, lower).upper()
            else:
                res += c
        return res

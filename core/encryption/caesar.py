import string

class CaesarCipher:
    ALPHABET_LOWER = string.ascii_lowercase
    ALPHABET_UPPER = string.ascii_uppercase
    M = 26

    def __init__(self, shift: int = 3):
        self.shift = shift

    def encrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                res += self.ALPHABET_LOWER[(self.ALPHABET_LOWER.index(c)+self.shift)%self.M]
            elif c.isupper():
                res += self.ALPHABET_UPPER[(self.ALPHABET_UPPER.index(c)+self.shift)%self.M]
            else:
                res += c
        return res

    def decrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                res += self.ALPHABET_LOWER[(self.ALPHABET_LOWER.index(c)-self.shift)%self.M]
            elif c.isupper():
                res += self.ALPHABET_UPPER[(self.ALPHABET_UPPER.index(c)-self.shift)%self.M]
            else:
                res += c
        return res

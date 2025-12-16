import string

class AffineCipher:
    ALPHABET_LOWER = string.ascii_lowercase
    ALPHABET_UPPER = string.ascii_uppercase
    M = 26

    def __init__(self, a=5, b=8):
        self.a = a
        self.b = b

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self.egcd(b % a, a)
        return g, x - (b // a) * y, y

    def modinv(self, a, m):
        g, x, _ = self.egcd(a, m)
        if g != 1:
            raise ValueError("No modular inverse for given a")
        return x % m

    def encrypt(self, text: str) -> str:
        res = ""
        for c in text:
            if c.islower():
                x = self.ALPHABET_LOWER.index(c)
                res += self.ALPHABET_LOWER[(self.a * x + self.b) % self.M]
            elif c.isupper():
                x = self.ALPHABET_UPPER.index(c)
                res += self.ALPHABET_UPPER[(self.a * x + self.b) % self.M]
            else:
                res += c
        return res

    def decrypt(self, text: str) -> str:
        a_inv = self.modinv(self.a, self.M)
        res = ""
        for c in text:
            if c.islower():
                y = self.ALPHABET_LOWER.index(c)
                res += self.ALPHABET_LOWER[(a_inv * (y - self.b)) % self.M]
            elif c.isupper():
                y = self.ALPHABET_UPPER.index(c)
                res += self.ALPHABET_UPPER[(a_inv * (y - self.b)) % self.M]
            else:
                res += c
        return res

import string

class VigenereCipher:
   
    ALPHABET_LOWER = string.ascii_lowercase
    ALPHABET_UPPER = string.ascii_uppercase
    M = 26

    def __init__(self, key: str = "KEY"):
        
        self.key = ''.join(k for k in key if k.isalpha())
        
        
        if not self.key:
            self.key = "KEY"

    def encrypt(self, text: str) -> str:
        res, ki = "", 0
        for c in text:
           
            if c.lower() in self.ALPHABET_LOWER:
                k = self.key[ki % len(self.key)]
                shift = self.ALPHABET_LOWER.index(k.lower())
                
                if c.islower():
                    res += self.ALPHABET_LOWER[(self.ALPHABET_LOWER.index(c) + shift) % self.M]
                else:
                    res += self.ALPHABET_UPPER[(self.ALPHABET_UPPER.index(c) + shift) % self.M]
                ki += 1
            else:
                
                res += c
        return res

    def decrypt(self, text: str) -> str:
        res, ki = "", 0
        for c in text:
        
            if c.lower() in self.ALPHABET_LOWER:
                k = self.key[ki % len(self.key)]
                shift = self.ALPHABET_LOWER.index(k.lower())
                
                if c.islower():
                   
                    res += self.ALPHABET_LOWER[(self.ALPHABET_LOWER.index(c) - shift) % self.M]
                else:
                    res += self.ALPHABET_UPPER[(self.ALPHABET_UPPER.index(c) - shift) % self.M]
                ki += 1
            else:
                res += c
        return res
import string

class PlayfairCipher:
    def __init__(self, key: str = "KEY"):
        self.key_matrix = self._generate_matrix(key)

    def _generate_matrix(self, key):
       
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key = key.upper().replace("J", "I")
       
        matrix_content = []
        for char in key:
            if char in alphabet and char not in matrix_content:
                matrix_content.append(char)
        
       
        for char in alphabet:
            if char not in matrix_content:
                matrix_content.append(char)
        
       
        return [matrix_content[i:i+5] for i in range(0, 25, 5)]

    def _find_position(self, char):
        for r, row in enumerate(self.key_matrix):
            for c, val in enumerate(row):
                if val == char:
                    return r, c
        return None

    def _process_text(self, text):
        text = text.upper().replace("J", "I")
      
        text = ''.join(filter(str.isalpha, text))
        
        processed = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = ""
            if i + 1 < len(text):
                b = text[i + 1]
            
           
            if a == b:
                processed += a + "X"
                i += 1
            elif b:
                processed += a + b
                i += 2
            else:
               
                processed += a + "X"
                i += 1
        return processed

    def _crypt(self, text, mode):
       
        text = self._process_text(text) if mode == 1 else text
        result = ""
        
        for i in range(0, len(text), 2):
            a, b = text[i], text[i+1]
            r1, c1 = self._find_position(a)
            r2, c2 = self._find_position(b)

            if r1 == r2: # Aynı satır
                result += self.key_matrix[r1][(c1 + mode) % 5]
                result += self.key_matrix[r2][(c2 + mode) % 5]
            elif c1 == c2: # Aynı sütun
                result += self.key_matrix[(r1 + mode) % 5][c1]
                result += self.key_matrix[(r2 + mode) % 5][c2]
            else: # Dikdörtgen
                result += self.key_matrix[r1][c2]
                result += self.key_matrix[r2][c1]
        
        return result

    def encrypt(self, text: str) -> str:
       
        if not text: return ""
        return self._crypt(text, 1)

    def decrypt(self, text: str) -> str:
        if not text: return ""
        
        return self._crypt(text, -1)
import string

class PolybiusCipher:
    def __init__(self, key: str = ""):
        
        self.grid = self._generate_grid(key)

    def _generate_grid(self, key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" 
        
        
        key = ''.join(filter(str.isalpha, key.upper())).replace("J", "I")
        
        unique_key = []
        for char in key:
            if char not in unique_key:
                unique_key.append(char)
        
       
        for char in alphabet:
            if char not in unique_key:
                unique_key.append(char)
        
        
        return unique_key

    def encrypt(self, text: str) -> str:
        if not text: return ""
        text = text.upper().replace("J", "I")
        result = ""
        
        for char in text:
            if char in self.grid:
                index = self.grid.index(char)
                row = (index // 5) + 1
                col = (index % 5) + 1
                result += f"{row}{col}"
            else:
              
                result += char
        return result

    def decrypt(self, text: str) -> str:
        if not text: return ""
        
        result = ""
        i = 0
        while i < len(text):
           
            if text[i].isdigit():
                if i + 1 < len(text) and text[i+1].isdigit():
                    row = int(text[i])
                    col = int(text[i+1])
                    
                   
                    if 1 <= row <= 5 and 1 <= col <= 5:
                        index = (row - 1) * 5 + (col - 1)
                        result += self.grid[index]
                        i += 2
                    else:
                        
                        result += "?"
                        i += 2
                else:
                    
                    result += text[i]
                    i += 1
            else:
                
                result += text[i]
                i += 1
                
        return result
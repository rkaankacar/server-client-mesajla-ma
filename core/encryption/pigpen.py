class PigpenCipher:
    def __init__(self):
        
        self.encode_map = {
            'A': '⌟', 'B': '⊔', 'C': '⌞',
            'D': '⊐', 'E': '□', 'F': '⊏',
            'G': '⌝', 'H': '⊓', 'I': '⌜',
            'J': '⌟•', 'K': '⊔•', 'L': '⌞•',
            'M': '⊐•', 'N': '□•', 'O': '⊏•',
            'P': '⌝•', 'Q': '⊓•', 'R': '⌜•',
            'S': '∨', 'T': '>', 'U': '<', 'V': '∧',
            'W': '∨•', 'X': '>•', 'Y': '<•', 'Z': '∧•'
        }
        
      
        self.decode_map = {v: k for k, v in self.encode_map.items()}

    def encrypt(self, text: str) -> str:
        if not text: return ""
        text = text.upper()
        res = []
        
        for char in text:
           
            res.append(self.encode_map.get(char, char))
            
      
        return "".join(res)

    def decrypt(self, text: str) -> str:
        if not text: return ""
        
        res = []
        i = 0
        n = len(text)
        
        while i < n:
         
            current = text[i]
            
           
            if i + 1 < n and text[i+1] == '•':
                symbol = current + '•'
                res.append(self.decode_map.get(symbol, symbol))
                i += 2
            else:
                
                res.append(self.decode_map.get(current, current))
                i += 1
                
        return "".join(res)
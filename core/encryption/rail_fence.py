class RailFenceCipher:
    def __init__(self, rails: int = 3):
        
        self.rails = max(2, int(rails))

    def encrypt(self, text: str) -> str:
        if not text: return ""
        
      
        fence = [[] for _ in range(self.rails)]
        rail = 0
        direction = 1 

        for char in text:
            fence[rail].append(char)
            rail += direction

           
            if rail == 0 or rail == self.rails - 1:
                direction *= -1

       
        return ''.join(''.join(row) for row in fence)

    def decrypt(self, text: str) -> str:
        if not text: return ""
        
       
        fence = [['\n' for _ in range(len(text))] for _ in range(self.rails)]
        direction = -1
        row, col = 0, 0

       
        for _ in range(len(text)):
            if row == 0 or row == self.rails - 1:
                direction *= -1
            
            fence[row][col] = '*'
            col += 1
            row += direction

        
        index = 0
        for r in range(self.rails):
            for c in range(len(text)):
                if fence[r][c] == '*' and index < len(text):
                    fence[r][c] = text[index]
                    index += 1

      
        result = []
        row, col = 0, 0
        direction = -1

        for _ in range(len(text)):
            if row == 0 or row == self.rails - 1:
                direction *= -1
            
            result.append(fence[row][col])
            col += 1
            row += direction

        return ''.join(result)
# -*- coding: utf-8 -*-
"""
AES-128 Manuel Implementation
S-box, SubBytes, ShiftRows, MixColumns, AddRoundKey işlemleri ile
tam bir AES-128 implementasyonu (kütüphane kullanmadan)
"""

import base64


class AESManualCipher:
    """
    Manuel AES-128 implementasyonu (ECB modu).
    - 10 round
    - 16 byte anahtar
    - S-box ve Inverse S-box
    - SubBytes, ShiftRows, MixColumns, AddRoundKey
    """
    
    # AES S-box (Substitution box)
    S_BOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]
    
    # Inverse S-box
    INV_S_BOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]
    
    # Round constants (Rcon)
    RCON = [
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
    ]
    
    def __init__(self, key: str = None):
        """
        Args:
            key: 16 karakterlik anahtar. Belirtilmezse varsayılan kullanılır.
        """
        if key is None:
            key = "DefaultAESKey123"
        
        # Key'i 16 byte'a ayarla
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\0')
        elif len(key_bytes) > 16:
            key_bytes = key_bytes[:16]
        
        self.key = list(key_bytes)
        self.round_keys = self._key_expansion()
    
    def _key_expansion(self):
        """AES Key Expansion algoritması - 11 round key üretir."""
        # 4x4 state olarak key (column-major order)
        key_schedule = [self.key[i:i+4] for i in range(0, 16, 4)]
        
        # 44 word (176 byte) üret
        words = []
        for i in range(4):
            words.append(key_schedule[i])
        
        for i in range(4, 44):
            temp = words[i-1].copy()
            
            if i % 4 == 0:
                # RotWord
                temp = temp[1:] + temp[:1]
                # SubWord
                temp = [self.S_BOX[b] for b in temp]
                # XOR with Rcon
                temp[0] ^= self.RCON[(i // 4) - 1]
            
            # XOR with word 4 positions earlier
            words.append([words[i-4][j] ^ temp[j] for j in range(4)])
        
        # 11 round key'e dönüştür
        round_keys = []
        for r in range(11):
            rk = []
            for col in range(4):
                rk.extend(words[r * 4 + col])
            round_keys.append(rk)
        
        return round_keys
    
    def _sub_bytes(self, state):
        """SubBytes: Her byte'ı S-box ile değiştir."""
        return [self.S_BOX[b] for b in state]
    
    def _inv_sub_bytes(self, state):
        """InvSubBytes: Her byte'ı Inverse S-box ile değiştir."""
        return [self.INV_S_BOX[b] for b in state]
    
    def _shift_rows(self, state):
        """
        ShiftRows: Satırları sola kaydır.
        State 4x4 matrix olarak column-major order.
        """
        # State'i matrixe çevir (row-major olarak düşün)
        matrix = [
            [state[0], state[4], state[8], state[12]],
            [state[1], state[5], state[9], state[13]],
            [state[2], state[6], state[10], state[14]],
            [state[3], state[7], state[11], state[15]]
        ]
        
        # Satırları kaydır
        matrix[1] = matrix[1][1:] + matrix[1][:1]  # 1 sola
        matrix[2] = matrix[2][2:] + matrix[2][:2]  # 2 sola
        matrix[3] = matrix[3][3:] + matrix[3][:3]  # 3 sola
        
        # Tekrar column-major order'a çevir
        result = []
        for col in range(4):
            for row in range(4):
                result.append(matrix[row][col])
        return result
    
    def _inv_shift_rows(self, state):
        """InvShiftRows: Satırları sağa kaydır."""
        matrix = [
            [state[0], state[4], state[8], state[12]],
            [state[1], state[5], state[9], state[13]],
            [state[2], state[6], state[10], state[14]],
            [state[3], state[7], state[11], state[15]]
        ]
        
        # Satırları sağa kaydır
        matrix[1] = matrix[1][-1:] + matrix[1][:-1]  # 1 sağa
        matrix[2] = matrix[2][-2:] + matrix[2][:-2]  # 2 sağa
        matrix[3] = matrix[3][-3:] + matrix[3][:-3]  # 3 sağa
        
        result = []
        for col in range(4):
            for row in range(4):
                result.append(matrix[row][col])
        return result
    
    def _xtime(self, a):
        """GF(2^8)'de 2 ile çarpma."""
        if a & 0x80:
            return ((a << 1) ^ 0x1b) & 0xff
        return (a << 1) & 0xff
    
    def _gf_mult(self, a, b):
        """GF(2^8)'de çarpma."""
        result = 0
        while b:
            if b & 1:
                result ^= a
            a = self._xtime(a)
            b >>= 1
        return result
    
    def _mix_columns(self, state):
        """MixColumns: Her sütunu GF(2^8)'de matris çarpımı ile karıştır."""
        result = [0] * 16
        
        for col in range(4):
            idx = col * 4
            s0, s1, s2, s3 = state[idx], state[idx+1], state[idx+2], state[idx+3]
            
            result[idx]   = self._gf_mult(2, s0) ^ self._gf_mult(3, s1) ^ s2 ^ s3
            result[idx+1] = s0 ^ self._gf_mult(2, s1) ^ self._gf_mult(3, s2) ^ s3
            result[idx+2] = s0 ^ s1 ^ self._gf_mult(2, s2) ^ self._gf_mult(3, s3)
            result[idx+3] = self._gf_mult(3, s0) ^ s1 ^ s2 ^ self._gf_mult(2, s3)
        
        return result
    
    def _inv_mix_columns(self, state):
        """InvMixColumns: MixColumns'un tersi."""
        result = [0] * 16
        
        for col in range(4):
            idx = col * 4
            s0, s1, s2, s3 = state[idx], state[idx+1], state[idx+2], state[idx+3]
            
            result[idx]   = self._gf_mult(0x0e, s0) ^ self._gf_mult(0x0b, s1) ^ self._gf_mult(0x0d, s2) ^ self._gf_mult(0x09, s3)
            result[idx+1] = self._gf_mult(0x09, s0) ^ self._gf_mult(0x0e, s1) ^ self._gf_mult(0x0b, s2) ^ self._gf_mult(0x0d, s3)
            result[idx+2] = self._gf_mult(0x0d, s0) ^ self._gf_mult(0x09, s1) ^ self._gf_mult(0x0e, s2) ^ self._gf_mult(0x0b, s3)
            result[idx+3] = self._gf_mult(0x0b, s0) ^ self._gf_mult(0x0d, s1) ^ self._gf_mult(0x09, s2) ^ self._gf_mult(0x0e, s3)
        
        return result
    
    def _add_round_key(self, state, round_key):
        """AddRoundKey: State ile round key'i XOR'la."""
        return [state[i] ^ round_key[i] for i in range(16)]
    
    def _pad(self, data):
        """PKCS7 padding uygula."""
        pad_len = 16 - (len(data) % 16)
        return data + [pad_len] * pad_len
    
    def _unpad(self, data):
        """PKCS7 padding'i kaldır."""
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 16:
            return data
        return data[:-pad_len]
    
    def _encrypt_block(self, block):
        """Tek bir 16 byte blok şifrele."""
        state = list(block)
        
        # Initial round
        state = self._add_round_key(state, self.round_keys[0])
        
        # Rounds 1-9
        for r in range(1, 10):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, self.round_keys[r])
        
        # Final round (no MixColumns)
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, self.round_keys[10])
        
        return state
    
    def _decrypt_block(self, block):
        """Tek bir 16 byte blok çöz."""
        state = list(block)
        
        # Initial round
        state = self._add_round_key(state, self.round_keys[10])
        
        # Rounds 9-1
        for r in range(9, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, self.round_keys[r])
            state = self._inv_mix_columns(state)
        
        # Final round
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, self.round_keys[0])
        
        return state
    
    def encrypt(self, plaintext: str) -> str:
        """
        Metni AES-128-ECB ile şifreler (manuel implementasyon).
        
        Args:
            plaintext: Şifrelenecek düz metin
            
        Returns:
            Base64 kodlanmış şifreli metin
        """
        if not plaintext:
            return ""
        
        try:
            # Byte listesine çevir
            data = list(plaintext.encode('utf-8'))
            
            # Padding uygula
            data = self._pad(data)
            
            # Blok blok şifrele
            ciphertext = []
            for i in range(0, len(data), 16):
                block = data[i:i+16]
                encrypted_block = self._encrypt_block(block)
                ciphertext.extend(encrypted_block)
            
            # Base64 kodla
            return base64.b64encode(bytes(ciphertext)).decode('utf-8')
            
        except Exception as e:
            return f"AES Manuel Şifreleme Hatası: {e}"
    
    def decrypt(self, ciphertext: str) -> str:
        """
        AES-128-ECB ile şifrelenmiş metni çözer.
        
        Args:
            ciphertext: Base64 kodlanmış şifreli metin
            
        Returns:
            Çözülmüş düz metin
        """
        if not ciphertext:
            return ""
        
        try:
            # Base64 decode
            data = list(base64.b64decode(ciphertext))
            
            # Blok blok çöz
            plaintext = []
            for i in range(0, len(data), 16):
                block = data[i:i+16]
                decrypted_block = self._decrypt_block(block)
                plaintext.extend(decrypted_block)
            
            # Unpad ve string'e çevir
            plaintext = self._unpad(plaintext)
            return bytes(plaintext).decode('utf-8')
            
        except Exception as e:
            return f"AES Manuel Çözme Hatası: {e}"
    
    def get_key_hex(self) -> str:
        """Anahtarı hex formatında döndürür."""
        return bytes(self.key).hex()


# Test
if __name__ == "__main__":
    cipher = AESManualCipher("TestKey123456789")
    
    original = "Merhaba Dünya! Bu manuel AES testi."
    encrypted = cipher.encrypt(original)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Orijinal: {original}")
    print(f"Şifreli: {encrypted}")
    print(f"Çözülmüş: {decrypted}")
    print(f"Anahtar (hex): {cipher.get_key_hex()}")
    print(f"Başarılı: {original == decrypted}")

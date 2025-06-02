class CaesarCipher:
    def __init__(self, shift: int):
        """
        Initialize the Caesar cipher with a specific shift value.
        
        Args:
            shift (int): The number of positions to shift each letter
        """
        self.shift = shift % 26  # Ensure shift is between 0 and 25
        
    def encrypt(self, text: str) -> str:
        """
        Encrypt the given text using the Caesar cipher.
        
        Args:
            text (str): The text to encrypt
            
        Returns:
            str: The encrypted text
        """
        result = []
        for char in text:
            if char.isalpha():
                # Determine the base ASCII value (a=97, A=65)
                base = ord('a') if char.islower() else ord('A')
                # Shift the character and wrap around if necessary
                shifted = (ord(char) - base + self.shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, text: str) -> str:
        """
        Decrypt the given text using the Caesar cipher.
        
        Args:
            text (str): The text to decrypt
            
        Returns:
            str: The decrypted text
        """
        # Decryption is just encryption with the negative shift
        self.shift = -self.shift
        result = self.encrypt(text)
        self.shift = -self.shift  # Restore original shift
        return result

def caesar_encrypt(text: str, shift: int) -> str:
    """
    Encrypt text using Caesar cipher.
    
    Args:
        text (str): Text to encrypt
        shift (int): Shift value
        
    Returns:
        str: Encrypted text
    """
    cipher = CaesarCipher(shift)
    return cipher.encrypt(text)

def caesar_decrypt(text: str, shift: int) -> str:
    """
    Decrypt text using Caesar cipher.
    
    Args:
        text (str): Text to decrypt
        shift (int): Shift value
        
    Returns:
        str: Decrypted text
    """
    cipher = CaesarCipher(shift)
    return cipher.decrypt(text)

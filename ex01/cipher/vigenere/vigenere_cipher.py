class VigenereCipher:
    def __init__(self):
        pass

    def vigenere_encrypt(self, plain_text: str, key: str) -> str:
        """
        Encrypt text using Vigenere cipher
        
        Args:
            plain_text (str): Text to encrypt
            key (str): Encryption key
            
        Returns:
            str: Encrypted text
        """
        result = []
        key = key.upper()  # Convert key to uppercase
        key_length = len(key)
        key_as_int = [ord(i) - ord('A') for i in key]  # Convert key to 0-25 range
        
        for i, char in enumerate(plain_text):
            if char.isalpha():
                # Determine the base ASCII value (a=97, A=65)
                base = ord('A') if char.isupper() else ord('a')
                # Get the key value for this position
                key_value = key_as_int[i % key_length]
                # Calculate the new character
                value = (ord(char) - base + key_value) % 26
                result.append(chr(value + base))
            else:
                result.append(char)
                
        return ''.join(result)

    def vigenere_decrypt(self, cipher_text: str, key: str) -> str:
        """
        Decrypt text using Vigenere cipher
        
        Args:
            cipher_text (str): Text to decrypt
            key (str): Decryption key
            
        Returns:
            str: Decrypted text
        """
        result = []
        key = key.upper()  # Convert key to uppercase
        key_length = len(key)
        key_as_int = [ord(i) - ord('A') for i in key]  # Convert key to 0-25 range
        
        for i, char in enumerate(cipher_text):
            if char.isalpha():
                # Determine the base ASCII value (a=97, A=65)
                base = ord('A') if char.isupper() else ord('a')
                # Get the key value for this position
                key_value = key_as_int[i % key_length]
                # Calculate the new character
                value = (ord(char) - base - key_value) % 26
                result.append(chr(value + base))
            else:
                result.append(char)
                
        return ''.join(result)

def vigenere_encrypt(text: str, key: str) -> str:
    """
    Encrypt text using Vigenere cipher.
    
    Args:
        text (str): Text to encrypt
        key (str): Encryption key
        
    Returns:
        str: Encrypted text
    """
    cipher = VigenereCipher()
    return cipher.vigenere_encrypt(text, key)

def vigenere_decrypt(text: str, key: str) -> str:
    """
    Decrypt text using Vigenere cipher.
    
    Args:
        text (str): Text to decrypt
        key (str): Decryption key
        
    Returns:
        str: Decrypted text
    """
    cipher = VigenereCipher()
    return cipher.vigenere_decrypt(text, key)
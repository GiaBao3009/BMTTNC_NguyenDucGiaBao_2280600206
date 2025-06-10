import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

def encrypt_message(key, message):
    """Encrypts a message using AES in CBC mode."""
    cipher = AES.new(key, AES.MODE_CBC)
    # Ensure message is encoded to bytes before padding
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)
    # The IV is prepended to the ciphertext
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    """Decrypts a message using AES in CBC mode."""
    # Extract the IV from the beginning of the message
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt and unpad the message
    decrypted_padded_message = cipher.decrypt(ciphertext)
    # Decode the bytes back to a string
    return unpad(decrypted_padded_message, AES.block_size).decode('utf-8')

def receive_messages(client_socket):
    """
    Listens for incoming messages from the server and prints them.
    This function runs in a separate thread.
    """
    while True:
        try:
            # Wait to receive a message from the server
            encrypted_message = client_socket.recv(2048)
            # If recv returns an empty string, the server has closed the connection
            if not encrypted_message:
                print("\nConnection closed by the server.")
                break

            # Decrypt and print the message
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            # Using \r to move cursor to the beginning of the line to not mess up input()
            print(f"\rReceived: {decrypted_message}\nEnter message ('exit' to quit): ", end="")

        except Exception as e:
            # An error occurred, likely because the connection was closed
            print(f"\nAn error occurred while receiving messages: {e}")
            break

def main():
    """Main function to run the client."""
    global aes_key # Make aes_key accessible to receive_messages

    # --- Initialization and Connection ---
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
        return # Exit if connection fails

    try:
        # --- Key Exchange ---
        # 1. Generate client's RSA key pair
        client_key = RSA.generate(2048)

        # 2. Receive server's public key
        server_public_key_pem = client_socket.recv(2048)
        server_public_key = RSA.import_key(server_public_key_pem)

        # 3. Send client's public key to the server
        client_socket.send(client_key.publickey().export_key(format='PEM'))

        # 4. Receive and decrypt the shared AES key
        encrypted_aes_key = client_socket.recv(2048)
        cipher_rsa = PKCS1_OAEP.new(client_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        print("Secure AES key exchanged.")

        # --- Start Receiving Messages ---
        # Start a thread to listen for messages from the server
        # It's a daemon thread so it will close automatically when the main program ends
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        receive_thread.start()

        # --- Send Messages Loop ---
        while True:
            message = input("Enter message ('exit' to quit): ")
            encrypted_message = encrypt_message(aes_key, message)
            client_socket.sendall(encrypted_message)
            
            if message.lower() == 'exit':
                break
    
    except Exception as e:
        print(f"An error occurred during communication: {e}")
    finally:
        # --- Cleanup ---
        print("Closing connection.")
        client_socket.close()

if __name__ == "__main__":
    main()

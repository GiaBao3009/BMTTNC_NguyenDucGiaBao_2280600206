import socket
import threading
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Use a try-except block to handle address already in use error
try:
    server_socket.bind(('localhost', 12345))
except socket.error as e:
    print(f"Error binding socket: {e}")
    exit()

server_socket.listen(5)
print("Server is listening for connections...")

# Generate server's RSA key pair
server_key = RSA.generate(2048)

# List to store connected clients (socket, aes_key)
clients = []
clients_lock = threading.Lock() # To safely modify the clients list from multiple threads

def broadcast(message, sender_socket):
    """Sends a message to all clients except the sender."""
    with clients_lock:
        # Create a snapshot of the clients to iterate over
        for client_socket, aes_key in clients:
            if client_socket != sender_socket:
                try:
                    encrypted_message = encrypt_message(aes_key, message)
                    client_socket.sendall(encrypted_message)
                except Exception as e:
                    print(f"Error broadcasting to a client: {e}")


def encrypt_message(key, message):
    """Encrypts a message using AES."""
    cipher = AES.new(key, AES.MODE_CBC)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    """Decrypts a message using AES."""
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_message = cipher.decrypt(ciphertext)
    return unpad(decrypted_padded_message, AES.block_size).decode('utf-8')

def handle_client(client_socket, client_address):
    """
    Handles a single client connection:
    1. Performs RSA key exchange.
    2. Generates and sends a shared AES key.
    3. Listens for messages and broadcasts them.
    """
    print(f"Connected with {client_address}")
    try:
        # --- RSA Key Exchange ---
        # 1. Send server's public key to client
        client_socket.send(server_key.publickey().export_key(format='PEM'))

        # 2. Receive client's public key
        client_public_key_pem = client_socket.recv(2048)
        client_public_key = RSA.import_key(client_public_key_pem)

        # --- AES Key Exchange ---
        # 3. Generate a new AES key for this client
        aes_key = get_random_bytes(16)

        # 4. Encrypt the AES key with the client's public key and send it
        cipher_rsa = PKCS1_OAEP.new(client_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        client_socket.send(encrypted_aes_key)

        # Add the new client to the list
        with clients_lock:
            clients.append((client_socket, aes_key))
        print(f"AES key exchanged with {client_address}")

        # --- Message Handling Loop ---
        while True:
            encrypted_message = client_socket.recv(2048)
            if not encrypted_message:
                break # Client disconnected

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")

            if decrypted_message.lower() == "exit":
                break
            
            # Broadcast the message to other clients
            broadcast_message = f"{client_address}: {decrypted_message}"
            broadcast(broadcast_message, client_socket)

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # --- Cleanup ---
        # Remove client from the list and close connection
        with clients_lock:
            # Find the client to remove
            client_to_remove = None
            for client in clients:
                if client[0] == client_socket:
                    client_to_remove = client
                    break
            if client_to_remove:
                clients.remove(client_to_remove)
        
        client_socket.close()
        print(f"Connection with {client_address} closed")

# Main loop to accept new connections
try:
    while True:
        client_socket, client_address = server_socket.accept()
        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("\nServer is shutting down.")
finally:
    server_socket.close()

from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.Vigenere import VigenereCipher

app = Flask(__name__)

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        plain_text = data.get('plain_text')
        key = data.get('key')

        if plain_text is None or key is None:
            return jsonify({'error': 'Missing plain_text or key'}), 400

        try:
            key = int(key)
        except ValueError:
            return jsonify({'error': 'Key must be an integer'}), 400

        cipher = CaesarCipher()  # Instantiate CaesarCipher without key here
        encrypted_text = cipher.encrypt_text(plain_text, key) # Use encrypt_text method
        return jsonify({'encrypted_message': encrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        cipher_text = data.get('cipher_text')
        key = data.get('key')

        if cipher_text is None or key is None:
            return jsonify({'error': 'Missing cipher_text or key'}), 400

        try:
            key = int(key)
        except ValueError:
            return jsonify({'error': 'Key must be an integer'}), 400

        cipher = CaesarCipher() # Instantiate CaesarCipher without key here
        decrypted_text = cipher.decrypt_text(cipher_text, key) # Use decrypt_text method
        return jsonify({'decrypted_message': decrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        plain_text = data.get('plain_text')
        key = data.get('key')

        if plain_text is None or key is None:
            return jsonify({'error': 'Missing plain_text or key'}), 400

        if not isinstance(key, str):
            return jsonify({'error': 'Key must be a string'}), 400

        cipher = VigenereCipher()
        encrypted_text = cipher.vigenere_encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        cipher_text = data.get('cipher_text')
        key = data.get('key')

        if cipher_text is None or key is None:
            return jsonify({'error': 'Missing cipher_text or key'}), 400

        if not isinstance(key, str):
            return jsonify({'error': 'Key must be a string'}), 400

        cipher = VigenereCipher()
        decrypted_text = cipher.vigenere_decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
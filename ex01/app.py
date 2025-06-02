import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'cipher'))
from flask import Flask, request, jsonify
from flask_cors import CORS
from caesar.caesar_cipher import caesar_encrypt, caesar_decrypt
from vigenere.vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from playfair.playfair_cipher import playfair_encrypt, playfair_decrypt, create_playfair_matrix
from railfence.railfence_cipher import railfence_encrypt, railfence_decrypt
from transposition.transposition_cipher import transposition_encrypt, transposition_decrypt



app = Flask(__name__)
# Cấu hình CORS chi tiết
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/caesar/encrypt', methods=['POST', 'OPTIONS'])
def caesar_encrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        key = int(data.get('key', 0))
        cipher_text = caesar_encrypt(plain_text, key)
        return jsonify({'cipher_text': cipher_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/caesar/decrypt', methods=['POST', 'OPTIONS'])
def caesar_decrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        key = int(data.get('key', 0))
        plain_text = caesar_decrypt(cipher_text, key)
        return jsonify({'plain_text': plain_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vigenere/encrypt', methods=['POST', 'OPTIONS'])
def vigenere_encrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        key = data.get('key', '')
        cipher_text = vigenere_encrypt(plain_text, key)
        return jsonify({'cipher_text': cipher_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vigenere/decrypt', methods=['POST', 'OPTIONS'])
def vigenere_decrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        key = data.get('key', '')
        plain_text = vigenere_decrypt(cipher_text, key)
        return jsonify({'plain_text': plain_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/playfair/encrypt', methods=['POST', 'OPTIONS'])
def playfair_encrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        key = data.get('key', '')
        cipher_text = playfair_encrypt(plain_text, key)
        return jsonify({'cipher_text': cipher_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/playfair/decrypt', methods=['POST', 'OPTIONS'])
def playfair_decrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        key = data.get('key', '')
        plain_text = playfair_decrypt(cipher_text, key)
        return jsonify({'plain_text': plain_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/playfair/create_matrix', methods=['POST', 'OPTIONS'])
def playfair_create_matrix_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        key = data.get('key', '')
        if not key:
            return jsonify({'error': 'Key is required'}), 400
        
        # Sử dụng hàm create_playfair_matrix từ module Playfair cipher
        matrix = create_playfair_matrix(key)
        return jsonify({'matrix': matrix})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/railfence/encrypt', methods=['POST', 'OPTIONS'])
def railfence_encrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        key = int(data.get('key', 0))
        cipher_text = railfence_encrypt(plain_text, key)
        return jsonify({'cipher_text': cipher_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/railfence/decrypt', methods=['POST', 'OPTIONS'])
def railfence_decrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        key = int(data.get('key', 0))
        plain_text = railfence_decrypt(cipher_text, key)
        return jsonify({'plain_text': plain_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transposition/encrypt', methods=['POST', 'OPTIONS'])
def transposition_encrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        key_str = data.get('key', '')
        try:
            key = int(key_str)
        except ValueError:
            return jsonify({'error': 'Invalid key: key must be an integer for Transposition cipher'}), 400
        cipher_text = transposition_encrypt(plain_text, key)
        return jsonify({'cipher_text': cipher_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transposition/decrypt', methods=['POST', 'OPTIONS'])
def transposition_decrypt_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        key_str = data.get('key', '')
        try:
            key = int(key_str)
        except ValueError:
            return jsonify({'error': 'Invalid key: key must be an integer for Transposition cipher'}), 400
        plain_text = transposition_decrypt(cipher_text, key)
        return jsonify({'plain_text': plain_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
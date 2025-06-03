import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import os
import rsa
import base64

# Thêm đường dẫn của thư mục gốc vào sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ui.rsa import Ui_MainWindow

if not os.path.exists('cipher/rsa/keys'):
    os.makedirs('cipher/rsa/keys')


class RSACipher:
    def __init__(self):
        pass

    def generate_keys(self):
        try:
            (public_key, private_key) = rsa.newkeys(1024)
            with open('cipher/rsa/keys/publicKey.pem', 'wb') as p:
                p.write(public_key.save_pkcs1('PEM'))
            with open('cipher/rsa/keys/privateKey.pem', 'wb') as p:
                p.write(private_key.save_pkcs1('PEM'))
            return True, "Keys generated successfully"
        except Exception as e:
            return False, f"Error generating keys: {str(e)}"

    def load_keys(self):
        try:
            with open('cipher/rsa/keys/publicKey.pem', 'rb') as p:
                public_key = rsa.PublicKey.load_pkcs1(p.read())
            with open('cipher/rsa/keys/privateKey.pem', 'rb') as p:
                private_key = rsa.PrivateKey.load_pkcs1(p.read())
            return True, (private_key, public_key)
        except FileNotFoundError:
            return False, "Keys not found. Please generate keys first."
        except Exception as e:
            return False, f"Error loading keys: {str(e)}"

    def encrypt(self, message, key):
        try:
            # RSA encrypts bytes, so encode message
            encrypted_message = rsa.encrypt(message.encode('utf-8'), key)
            # Return base64 encoded bytes to display as string
            return True, base64.b64encode(encrypted_message).decode('utf-8')
        except Exception as e:
            return False, f"Error encrypting message: {str(e)}"

    def decrypt(self, ciphertext, key):
        try:
            # Decode base64 string back to bytes
            ciphertext_bytes = base64.b64decode(ciphertext.encode('utf-8'))
            # RSA decrypts bytes
            decrypted_message = rsa.decrypt(ciphertext_bytes, key).decode('utf-8')
            return True, decrypted_message
        except Exception as e:
            return False, f"Error decrypting message: {str(e)}"

    def sign(self, message, key):
        try:
            # RSA signs bytes
            signature_bytes = rsa.sign(message.encode('utf-8'), key, 'SHA-256') # Using SHA-256 for better security
            # Return base64 encoded bytes to display as string
            return True, base64.b64encode(signature_bytes).decode('utf-8')
        except Exception as e:
            return False, f"Error signing message: {str(e)}"

    def verify(self, message, signature_base64, key):
        try:
            # Decode base64 string back to bytes
            signature_bytes = base64.b64decode(signature_base64.encode('utf-8'))
            # RSA verifies bytes
            rsa.verify(message.encode('utf-8'), signature_bytes, key)
            return True, True # Verification successful, rsa.verify returns None on success
        except rsa.VerificationError:
            return True, False # Verification failed specifically
        except Exception as e:
            return False, f"Error verifying signature: {str(e)}"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rsa = RSACipher()

        # Kết nối các nút với các hàm xử lý tương ứng
        self.ui.btn_generate.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        success, message = self.rsa.generate_keys()
        if success:
            self._show_success(message)
        else:
            self._show_error(message)

    def call_api_encrypt(self):
        success, keys = self.rsa.load_keys()
        if not success:
            self._show_error(keys)
            return

        plain_text = self.ui.text_plaintext.toPlainText()
        if not plain_text:
            self._show_error("Please enter text to encrypt.")
            return

        success, result = self.rsa.encrypt(plain_text, keys[1])  # Use public key
        if success:
            self.ui.txt_ciphertext.setText(result)
            self._show_success("Encrypted Successfully")
        else:
            self._show_error(result)

    def call_api_decrypt(self):
        success, keys = self.rsa.load_keys()
        if not success:
            self._show_error(keys)
            return

        cipher_text = self.ui.txt_ciphertext.toPlainText()
        if not cipher_text:
             self._show_error("Please enter text to decrypt.")
             return

        success, result = self.rsa.decrypt(cipher_text, keys[0])  # Use private key
        if success:
            self.ui.text_plaintext.setText(result)
            self._show_success("Decrypted Successfully")
        else:
            self._show_error(result)

    def call_api_sign(self):
        success, keys = self.rsa.load_keys()
        if not success:
            self._show_error(keys)
            return

        info_text = self.ui.txt_info.toPlainText()
        if not info_text:
            self._show_error("Please enter information to sign.")
            return

        success, result = self.rsa.sign(info_text, keys[0])  # Use private key
        if success:
            self.ui.txt_sign.setText(result)
            self._show_success("Signed Successfully")
        else:
            self._show_error(result)

    def call_api_verify(self):
        success, keys = self.rsa.load_keys()
        if not success:
            self._show_error(keys)
            return

        info_text = self.ui.txt_info.toPlainText()
        sign_text = self.ui.txt_sign.toPlainText()

        if not info_text or not sign_text:
             self._show_error("Please enter both information and signature to verify.")
             return

        success, result = self.rsa.verify(
            info_text,
            sign_text,
            keys[1]  # Use public key
        )
        if success:
            if result:
                self._show_success("Verified Successfully")
            else:
                self._show_error("Verified Fail: Signature does not match.") # More specific error message
        else:
            self._show_error(result)

    def _show_success(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec_()

    def _show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
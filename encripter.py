from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature

CRYPT_KEY = Fernet.generate_key()

class Crypt:

    @staticmethod
    def encrypt(text):
        cipher_suite = Fernet(CRYPT_KEY)
        cipher_text = cipher_suite.encrypt(text.encode('utf-8'))

        return cipher_text

    @staticmethod
    def decrypt(cipher_text):
        try:
            cipher_suite = Fernet(CRYPT_KEY)
            plain_text = cipher_suite.decrypt(cipher_text).decode('utf-8')

            return plain_text
        except InvalidSignature:
            raise RuntimeError('Chave de criptografia mudou - Necessario recadastrar administrador!')


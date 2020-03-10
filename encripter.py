from cryptography.fernet import Fernet

CRYPT_KEY = Fernet.generate_key()

class Crypt:

    @staticmethod
    def encrypt(text):
        cipher_suite = Fernet(CRYPT_KEY)
        cipher_text = cipher_suite.encrypt(text.encode('utf-8'))

        return cipher_text

    @staticmethod
    def decrypt(cipher_text):

        plain_text = cipher_suite.decrypt(cipher_text).decode('utf-8')

        return plain_text


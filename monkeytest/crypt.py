from cryptography.fernet import Fernet
from ressources import *
import cffi

key = b'A2uVpN1aJpTRPKaOa2v4HGVut7qIGoVHrYuuv79W2GY='

def encrypt(data, name):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    file = open(name,'wb')
    file.write(encrypted_data)
    file.close()

def decrypt(path=""):
    fernet = Fernet(key)
    if path != "":
        file = open(path, 'rb')
        encrypted_data = file.read()
    else:
        encrypted_data = wbank
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')


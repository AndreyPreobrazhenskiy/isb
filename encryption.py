import os
from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import padding, hashes


def encrypt_file(settings: Dict[str, str]) -> None:
    """
    Encrypts a file using an RSA-encrypted symmetric key (AES) and stores the result.

    :param settings: A dictionary containing the following keys:
        - 'symmetric_key': Path to the encrypted symmetric key file.
        - 'secret_key': Path to the RSA private key used for decrypting the symmetric key.
        - 'initial_file': Path to the file to be encrypted.
        - 'encrypted_file': Path to save the encrypted file.
    :return: None
    """

    print("[*] Загрузка зашифрованного симм. ключа...")
    with open(settings['symmetric_key'], 'rb') as f:
        encrypted_key = f.read()

    print("[*] Загрузка закрытого ключа RSA...")
    with open(settings['secret_key'], 'rb') as f:
        private_key = load_pem_private_key(f.read(), password=None)

    print("[*] Расшифровка симметричного ключа...")
    symmetric_key = private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("[*] Чтение исходного файла и паддинг...")
    with open(settings['initial_file'], 'rb') as f:
        plaintext = f.read()

    padder = padding.ANSIX923(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    print("[*] Шифрование файла...")
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    with open(settings['encrypted_file'], 'wb') as f:
        f.write(iv + ciphertext)

    print("[+] Файл зашифрован и сохранён.")

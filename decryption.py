from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import padding, hashes


def decrypt_file(settings: Dict[str, str]) -> None:
    """
    Decrypts an encrypted file using an RSA-encrypted AES symmetric key.

    :param settings: A dictionary with the following keys:
        - 'symmetric_key': Path to the file containing the encrypted symmetric key.
        - 'secret_key': Path to the PEM-encoded RSA private key file.
        - 'encrypted_file': Path to the AES-encrypted file.
        - 'decrypted_file': Path to save the decrypted output file.
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

    print("[*] Загрузка зашифрованного файла...")
    with open(settings['encrypted_file'], 'rb') as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    print("[*] Дешифрование и удаление паддинга...")
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.ANSIX923(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(settings['decrypted_file'], 'wb') as f:
        f.write(plaintext)

    print("[+] Файл расшифрован и сохранён.")

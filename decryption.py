from typing import Dict
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding


def decrypt_file(settings: Dict[str, str]) -> None:
    """
    Decrypts a file encrypted with a symmetric SEED key, where the key was originally encrypted with RSA.

    :param settings: A dictionary with the following keys:
        - 'symmetric_key': Path to the RSA-encrypted symmetric key file.
        - 'secret_key': Path to the PEM-encoded RSA private key file used for decrypting the symmetric key.
        - 'encrypted_file': Path to the file that contains the IV and SEED-encrypted data.
        - 'decrypted_file': Path to save the decrypted plaintext output.
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

    cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    print("[*] Дешифрование и удаление паддинга...")
    unpadder = sym_padding.ANSIX923(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(settings['decrypted_file'], 'wb') as f:
        f.write(plaintext)

    print("[+] Файл расшифрован и сохранён.")

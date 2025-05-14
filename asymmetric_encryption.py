import os
from typing import Dict
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes
from file_manager import FileManager


class AsymetricEncryption:
    @staticmethod
    def generate_keys(settings: Dict[str, str]) -> None:
        """
        Generates an RSA key pair and a symmetric AES key.
        The symmetric key is encrypted with the RSA public key and saved to a file.
        :param settings: A dictionary containing the following keys:
            - 'symmetric_key': Path to save the encrypted symmetric key.
            - 'public_key': Path to save the public RSA key.
            - 'secret_key': Path to save the private RSA key.
        :return: None
        """

        print("[*] Генерация симметричного ключа...")
        sym_key = os.urandom(16)
        print("[+] Симметричный ключ сгенерирован.")

        print("[*] Генерация асимметричных ключей...")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        print("[*] Сериализация ключей...")
        FileManager.save_public_key(public_key)
        FileManager.save_private_key(private_key)

        print("[*] Шифрование симметричного ключа...")
        encrypted_sym_key = public_key.encrypt(
            sym_key,
            asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        with open(settings['symmetric_key'], 'wb') as f:
            f.write(encrypted_sym_key)

        print("[+] Генерация и шифрование ключей завершены.")

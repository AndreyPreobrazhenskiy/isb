import os
from cryptography.hazmat.primitives import serialization


class FileManager:
    @staticmethod
    def check_files_exist(paths: list) -> None:
        """
        Checks whether the specified files exist.
        :param paths: List of file paths to check.
        :raises SystemExit: If any file is not found.
        """

        for path in paths:
            if not os.path.exists(path):
                print(f"[!] Не найден файл: {path}")
                exit(1)


    @staticmethod
    def save_public_key(public_key) -> None:
        with open('public_key.txt', 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    @staticmethod
    def save_private_key(private_key) -> None:
        with open('private_key.txt', 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

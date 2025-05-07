import argparse
import json
import os
from key_generation import generate_keys
from encryption import encrypt_file
from decryption import decrypt_file

def load_settings() -> dict:
    """
    Loads the settings from a JSON configuration file.

    :return: Dictionary containing configuration settings.
    :raises SystemExit: If the settings.json file is not found.
    """

    try:
        with open('settings.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] Файл settings.json не найден.")
        exit(1)

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

def main() -> None:
    parser = argparse.ArgumentParser(description="Гибридная криптосистема")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование данных')
    group.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование данных')

    args = parser.parse_args()
    settings = load_settings()

    if args.generation:
        print("[*] Генерация ключей...")
        generate_keys(settings)
        print("[+] Ключи успешно сгенерированы.")

    elif args.encryption:
        print("[*] Подготовка к шифрованию...")
        check_files_exist([settings['symmetric_key'], settings['secret_key'], settings['initial_file']])
        encrypt_file(settings)
        print(f"[+] Файл зашифрован: {settings['encrypted_file']}")

    elif args.decryption:
        print("[*] Подготовка к дешифрованию...")
        check_files_exist([settings['symmetric_key'], settings['secret_key'], settings['encrypted_file']])
        decrypt_file(settings)
        print(f"[+] Файл расшифрован: {settings['decrypted_file']}")

if __name__ == "__main__":
    main()

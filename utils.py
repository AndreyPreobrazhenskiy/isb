import json
import argparse


class Utils:
    @staticmethod
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


    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Гибридная криптосистема")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
        group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование данных')
        group.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование данных')
        return parser.parse_args()

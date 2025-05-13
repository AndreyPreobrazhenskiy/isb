from utils import load_settings
from utils import parse_args
from file_manager import check_files_exist
from asymmetric_encryption import generate_keys
from symmetric_encryption import encrypt_file
from symmetric_encryption import decrypt_file


def main() -> None:
    args = parse_args()
    settings = load_settings()

    if args.generation:
        print("[*] Генерация ключей...")
        generate_keys(settings)
        print("[+] Ключи успешно сгенерированы.")

    elif args.encryption:
        print("[*] Подготовка к шифрованию...")
        check_files_exist([settings['symmetric_key'], settings['secret_key'], settings['initial_file']])
        encrypt_file(settings)

    elif args.decryption:
        print("[*] Подготовка к дешифрованию...")
        check_files_exist([settings['symmetric_key'], settings['secret_key'], settings['encrypted_file']])
        decrypt_file(settings)


if __name__ == "__main__":
    main()

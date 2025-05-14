from utils import Utils
from file_manager import FileManager
from asymmetric_encryption import AsymetricEncryption
from symmetric_encryption import SymmetricEncryption


def main() -> None:
    args = Utils.parse_args()
    settings = Utils.load_settings()

    if args.generation:
        print("[*] Генерация ключей...")
        AsymetricEncryption.generate_keys(settings)
        print("[+] Ключи успешно сгенерированы.")

    elif args.encryption:
        print("[*] Подготовка к шифрованию...")
        FileManager.check_files_exist([settings['symmetric_key'], settings['secret_key'], settings['initial_file']])
        SymmetricEncryption.encrypt_file(settings)

    elif args.decryption:
        print("[*] Подготовка к дешифрованию...")
        FileManager.check_files_exist([settings['symmetric_key'], settings['secret_key'], settings['encrypted_file']])
        SymmetricEncryption.decrypt_file(settings)


if __name__ == "__main__":
    main()

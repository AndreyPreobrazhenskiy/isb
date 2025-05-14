import os


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

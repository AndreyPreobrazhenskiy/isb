from typing import Optional, Tuple, Dict

from alphabet import ALPHABET
from funcs import prepare_text, save_to_file, read_file


def atbash_encrypt(text: str, key: Optional[str] = None) -> Tuple[str, str]:
    """
    Encrypts text using a modified Atbash cipher.

    :param text: The input text to be encrypted.
    :param key: The key used to generate the alphabet (optional).
    :return: A tuple (encrypted text, letter mapping string).
    """
    prepared: str = prepare_text(text)

    if key is None:
        alphabet: list[str] = list(ALPHABET)
    else:
        alphabet: list[str] = []
        for char in key.upper():
            if char not in alphabet and char in ALPHABET:
                alphabet.append(char)

        for char in ALPHABET:
            if char not in alphabet:
                alphabet.append(char)

    reversed_alphabet: list[str] = alphabet[::-1]
    mapping: dict[int, int] = str.maketrans(''.join(alphabet), ''.join(reversed_alphabet))
    encrypted_text: str = prepared.translate(mapping)

    key_mapping: str = "\n".join(f"{a} - {b}" for a, b in zip(alphabet, reversed_alphabet))

    return encrypted_text, key_mapping

def run_task1(input_file: str, output_prefix: str, key: Optional[str] = None) -> Dict[str, str]:
    """
    Reads an input file, encrypts the content, and saves the results.

    :param input_file: Path to the input text file.
    :param output_prefix: Prefix for the output file names.
    :param key: Encryption key (optional).
    :return: A dictionary with paths to the generated files.
    """
    input_text: str = read_file(input_file)
    encrypted: str
    key_mapping: str
    encrypted, key_mapping = atbash_encrypt(input_text, key)

    save_to_file(f"{output_prefix}_original.txt", input_text)
    save_to_file(f"{output_prefix}_encrypted.txt", encrypted)
    save_to_file(f"{output_prefix}_key.txt", key_mapping)

    return {
        "original_file": f"{output_prefix}_original.txt",
        "encrypted_file": f"{output_prefix}_encrypted.txt",
        "key_file": f"{output_prefix}_key.txt"
    }

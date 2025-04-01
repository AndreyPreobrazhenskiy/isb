from funcs import prepare_text, save_to_file, read_file
from alphabet import ALPHABET


def atbash_encrypt(text, key=None):
    """
    Encrypts text using a modified Atbash cipher.

    :param text: The input text to be encrypted.
    :param key: The key used to generate the alphabet (optional).
    :return: A tuple (encrypted text, letter mapping string).
    """
    prepared = prepare_text(text)

    if key is None:
        alphabet = list(ALPHABET)
    else:
        alphabet = []
        for char in key.upper():
            if char not in alphabet and char in ALPHABET:
                alphabet.append(char)

        for char in ALPHABET:
            if char not in alphabet:
                alphabet.append(char)

    reversed_alphabet = alphabet[::-1]
    mapping = str.maketrans(''.join(alphabet), ''.join(reversed_alphabet))
    encrypted_text = prepared.translate(mapping)

    key_mapping = "\n".join(f"{a} - {b}" for a, b in zip(alphabet, reversed_alphabet))

    return encrypted_text, key_mapping
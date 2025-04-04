import json
from collections import Counter
from typing import Dict, Tuple

from funcs import save_to_file, read_file


def load_reference_frequencies(filename: str) -> Dict[str, float]:
    """
    Loads a reference frequency table from a JSON file.

    :param filename: The path to the JSON file containing reference frequencies.
    :return: A dictionary of character frequencies.
    """
    with open(filename, mode='r', encoding='utf-8') as file:
        return json.load(file)


def calculate_frequencies(text: str) -> Dict[str, float]:
    """
    Calculates character frequency in a given text.

    :param text: The input text for frequency analysis.
    :return: A dictionary of character frequencies.
    """
    freq = Counter(text)
    total_chars = sum(freq.values())
    return {char: round(count / total_chars, 6) for char, count in freq.items() if char != "\n"}


def save_frequencies(freq_dict: Dict[str, float], filename: str) -> None:
    """
    Saves character frequency analysis to a JSON file, sorted by frequency descending.

    :param freq_dict: Dictionary containing character frequencies.
    :param filename: The path to the JSON file to save data.
    """
    sorted_freq = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(sorted_freq, file, ensure_ascii=False, indent=2)


def create_mapping(cipher_freq: Dict[str, float], reference_freq: Dict[str, float]) -> Dict[str, str]:
    """
    Creates a mapping between cipher text characters and reference frequencies.

    :param cipher_freq: Frequency dictionary from the cipher text.
    :param reference_freq: Reference frequency dictionary.
    :return: A dictionary mapping cipher characters to reference characters.
    """
    sorted_cipher_freq = sorted(cipher_freq.items(), key=lambda item: item[1], reverse=True)
    sorted_reference_freq = sorted(reference_freq.items(), key=lambda item: item[1], reverse=True)

    return {cipher_char: ref_char for (cipher_char, _), (ref_char, _) in zip(sorted_cipher_freq, sorted_reference_freq)}


def decode_text(text: str, mapping: Dict[str, str]) -> str:
    """
    Deciphers the text using the provided character mapping.

    :param text: The encrypted text.
    :param mapping: The character mapping dictionary.
    :return: The decrypted text.
    """
    return ''.join(mapping.get(char, char) if char != '\n' else ' ' for char in text)


def frequency_decrypt(cipher_text: str, freq_file: str, reference_freq: Dict[str, float]) -> Tuple[str, Dict[str, str]]:
    """
    Decrypts text using frequency analysis and creates a mapping.

    :param cipher_text: The encrypted text.
    :param freq_file: Path to save the calculated character frequencies.
    :param reference_freq: The reference character frequency dictionary.
    :return: A tuple (decrypted text, character mapping dictionary).
    """
    cipher_freq = calculate_frequencies(cipher_text)
    save_frequencies(cipher_freq, freq_file)

    mapping = create_mapping(cipher_freq, reference_freq)
    decrypted_text = decode_text(cipher_text, mapping)

    return decrypted_text, mapping


def run_task2(input_file: str, output_prefix: str, reference_freq_file: str) -> Dict[str, str]:
    """
    Runs frequency analysis and decryption.

    :param input_file: Path to the input file containing encrypted text.
    :param output_prefix: Prefix for output file names.
    :param reference_freq_file: Path to the reference frequency JSON file.
    :return: A dictionary containing paths to output files.
    """
    reference_freq = load_reference_frequencies(reference_freq_file)
    cipher_text = read_file(input_file)

    freq_file = f"{output_prefix}_frequencies.json"
    decrypted_text, mapping = frequency_decrypt(cipher_text, freq_file, reference_freq)

    save_to_file(f"{output_prefix}_decrypted.txt", decrypted_text)
    with open(f"{output_prefix}_mapping.json", mode='w', encoding='utf-8') as file:
        json.dump(mapping, file, ensure_ascii=False, indent=2)

    return {
        "decrypted_file": f"{output_prefix}_decrypted.txt",
        "mapping_file": f"{output_prefix}_mapping.json",
        "frequency_file": freq_file
    }


def decode_with_mapping_file(input_file: str, mapping_file: str, output_file: str) -> None:
    """
    Decodes the given text file using a character mapping from a JSON file.

    :param input_file: Path to the encrypted input text file.
    :param mapping_file: Path to the JSON file containing the character mapping.
    :param output_file: Path to save the decoded text.
    """
    cipher_text = read_file(input_file)

    with open(mapping_file, mode='r', encoding='utf-8') as file:
        mapping = json.load(file)

    decrypted_text = decode_text(cipher_text, mapping)
    save_to_file(output_file, decrypted_text)

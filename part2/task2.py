import json
from collections import Counter
from typing import Dict

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


def decode_text(text: str, mapping: Dict[str, str]) -> str:
    """
    Deciphers the text using the provided character mapping.

    :param text: The encrypted text.
    :param mapping: The character mapping dictionary.
    :return: The decrypted text.
    """
    return ''.join(mapping.get(char, char) if char != '\n' else ' ' for char in text)


def run_task2(input_file: str, output_prefix: str) -> Dict[str, str]:
    """
    Runs frequency analysis and decryption.

    :param input_file: Path to the input file containing encrypted text.
    :param output_prefix: Prefix for output file names.
    :return: A dictionary containing paths to output files.
    """
    cipher_text = read_file(input_file)
    freq_dict = calculate_frequencies(cipher_text)
    freq_file = f"{output_prefix}_frequencies.json"
    save_frequencies(freq_dict, freq_file)

    return { "frequency_file": freq_file }


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

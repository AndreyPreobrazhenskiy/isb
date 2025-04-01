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
    return {char: count / total_chars for char, count in freq.items()}
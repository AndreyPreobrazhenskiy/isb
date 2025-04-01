from pathlib import Path
from alphabet import ALPHABET

def prepare_text(text):
    """
    Cleans the text based on the alphabet.

    :param text: The input text to be cleaned.
    :return: The cleaned text containing only characters from the alphabet.
    """
    return ''.join(c.upper() for c in text if c.upper() in ALPHABET)

def read_file(filename):
    """
    Reads a file and handles errors if the file is not found.

    :param filename: The path to the file to be read.
    :return: The contents of the file as a string.
    :raises FileNotFoundError: If the file does not exist.
    """
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError as error:
        raise FileNotFoundError(f"File {filename} not found") from error

def save_to_file(filename, content):
    """
    Writes content to a file, creating directories if necessary.

    :param filename: The path to the file to be written.
    :param content: The content to be written to the file.
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(content)
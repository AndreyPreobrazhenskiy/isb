import math
from scipy.special import gammainc
from consts import *

def read_file(filename: str) -> str:
    """
    Reads the sequence
    :param filename: Path to the file to read.
    :return: The sequence
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


def write_file(filename: str, text: str) -> None:
    """
    Writes the given text to a file.
    :param filename: Path to the file to write to.
    :param text: The text
    :return: None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing file: {e}")


def frequency_bit_test(sequence: str) -> float:
    """
    Performs a frequency bit test
    :param sequence: The bit sequence
    :return: P-value
    """
    n = len(sequence)
    if n == 0:
        raise ValueError("Sequence is empty")
    s = sum([1 if bit == "1" else -1 for bit in sequence])
    p_value = math.erfc((abs(s) / math.sqrt(n)) / math.sqrt(2))
    return p_value


def runs_test(sequence: str) -> float:
    """
    Performs a test for identical consecutive bits.
    :param sequence: The sequence
    :return: P-value
    """
    n = len(sequence)
    p = sequence.count('1') / n

    if abs(p - 0.5) >= 2 / math.sqrt(n):
        return 0.0  # Not random enough for runs test

    v_n = 1
    for i in range(1, n):
        if sequence[i] != sequence[i - 1]:
            v_n += 1

    numerator = abs(v_n - 2 * n * p * (1 - p))
    denominator = 2 * math.sqrt(2 * n) * p * (1 - p)
    return math.erfc(numerator / denominator)


def block_run_test(sequence: str) -> float:
    """
    Performs a test for the longest sequence of ones in a block.
    :param sequence: The sequence
    :return: P-value
    """
    n = len(sequence)
    if n < 128:
        raise ValueError("Minimum 128 bits required")

    N = n // 8  # 8-bit blocks
    v = [0, 0, 0, 0]  # frequency counters

    for i in range(N):
        block = sequence[i * 8 : (i + 1) * 8]
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    x_2 = 0.0
    for i in range(len(v)):
        expected = 16 * PI[i]
        x_2 += (v[i] - expected) ** 2 / expected

    return gammainc(3 / 2, x_2 / 2)


def run_all_tests(sequence: str, label: str, output_file: str):
    """
    Runs all NIST tests on the given sequence and saves the result.
    """
    p1 = frequency_bit_test(sequence)
    p2 = runs_test(sequence)
    p3 = block_run_test(sequence)

    result = (
        f"{label} sequence:\n{sequence}\n\n"
        f"Frequency bit test (P-value): {p1:.17f}\n"
        f"Test for identical consecutive bits (P-value): {p2:.17f}\n"
        f"Test for the longest sequence of ones in a block (P-value): {p3:.17f}\n"
    )

    write_file(output_file, result)


def main():
    cpp_sequence = read_file(cpp_sequence_txt)
    java_sequence = read_file(java_sequence_txt)
    python_sequence = read_file(python_sequence_txt)

    run_all_tests(cpp_sequence, "C++", test_results_cpp)
    run_all_tests(java_sequence, "Java", test_results_java)
    run_all_tests(python_sequence, "Python", test_results_python)


if __name__ == "__main__":
    main()

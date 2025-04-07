import argparse
from pathlib import Path

from part1.task1 import run_task1
from part2.task2 import run_task2, decode_with_mapping_file


def parse_args():
    """
    Parse command-line arguments for the encryption and decryption tasks.

    :return: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='File processing: encryption and decryption')
    parser.add_argument('--input1', required=True, help='Input file for Task 1')
    parser.add_argument('--input2', required=True, help='Input file for Task 2')
    parser.add_argument('--reference_freq_file', required=False, help='Reference frequency file (optional)')
    parser.add_argument('--output_dir', default='output', help='Directory for results')
    parser.add_argument('--mapping_decrypt_input', required=True, help='Text file to decode using existing mapping')
    parser.add_argument('--mapping_file', required=True, help='JSON file with saved character mapping')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    output_task1 = Path(args.output_dir) / "task1"
    output_task2 = Path(args.output_dir) / "task2"

    output_task1.mkdir(parents=True, exist_ok=True)
    output_task2.mkdir(parents=True, exist_ok=True)

    print("Executing Task 1...")
    result1 = run_task1(args.input1, str(output_task1))

    print("\nExecuting Task 2 (frequency analysis only)...")
    result2 = run_task2(args.input2, str(output_task2))

    print("\nExecuting Task 3 (mapped decryption)...")
    decoded_output_path = Path(args.output_dir) / "mapping_decrypted.txt"
    decode_with_mapping_file(args.mapping_decrypt_input, args.mapping_file, str(decoded_output_path))

    print("\nResults:")
    print(f"1. Encrypted file: {result1['encrypted_file']}")
    print(f"   Encryption key: {result1['key_file']}")
    print(f"2. Frequency file: {result2['frequency_file']}")
    print(f"3. Mapped decryption output: {decoded_output_path}")

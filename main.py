import argparse

from part1.task1 import run_task1
from part2.task2 import run_task2


def parse_args():
    """
    Parses command-line arguments.

    :return: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='File processing: encryption and decryption')
    parser.add_argument('--input1', required=True, help='Input file for Task 1')
    parser.add_argument('--input2', required=True, help='Input file for Task 2')
    parser.add_argument('--reference_freq_file', required=True, help='Reference frequency file')
    parser.add_argument('--output_dir', default='output', help='Directory for results')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    print("Executing Task 1...")
    result1 = run_task1(args.input1, f"{args.output_dir}/task1")

    print("\nExecuting Task 2...")
    result2 = run_task2(args.input2, f"{args.output_dir}/task2", args.reference_freq_file)

    print("\nResults:")
    print(f"1. Encrypted file: {result1['encrypted_file']}")
    print(f"   Encryption key: {result1['key_file']}")
    print(f"2. Decrypted file: {result2['decrypted_file']}")
    print(f"   Mapping table: {result2['mapping_file']}")
    print(f"   Frequency file: {result2['frequency_file']}")

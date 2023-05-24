import argparse

from .extract_api import extract_apis
from .sequence_generator import get_sequences
from .test_generator import Generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Django Integration Testing Setup Generation Tool."
    )
    parser.add_argument("-m", "--managepy", type=str, required=True)
    parser.add_argument("-t", "--test-dir", type=str, required=True)
    parser.add_argument("-h", "--help", required=False)

    args = parser.parse_args()

    if args.help:
        print("help")
        exit(0)

    managepy_path = args.managepy
    test_dir_path = args.test_dir

    apis = extract_apis(managepy_path)
    sequences = get_sequences(apis)
    Generator.gen_test_file(
        filename="some_filename.py",
        testcasename="MyTestCase",
        sequences=sequences,
    )

    # TODO: evaluate and report
    # maybe we should save only "valid" tests?

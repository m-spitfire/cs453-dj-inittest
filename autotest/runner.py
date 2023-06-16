import argparse
from pprint import PrettyPrinter, pprint

from extract_api import extract_apis
from sequence_generator import get_sequences
from test_generator import Generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Django Integration Testing Setup Generation Tool."
    )
    parser.add_argument(
        "-m", "--managepy", type=str, required=True, help="path for manage.py"
    )
    parser.add_argument(
        "-t", "--test-filename", type=str, required=True, help="test filename"
    )
    parser.add_argument("-c", "--class-name", type=str, required=True)
    args = parser.parse_args()

    managepy_path = args.managepy
    test_filename = args.test_filename
    t_class_name = args.class_name

    apis = extract_apis(managepy_path)
    sequences = get_sequences(apis)

    Generator.gen_test_file(
        filename=test_filename,
        testcasename=t_class_name,
        sequences=sequences,
    )

    # TODO: evaluate and report
    # maybe we should save only "valid" tests?

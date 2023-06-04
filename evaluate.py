import importlib
import os
import unittest

import coverage
import django


def discover_test_case_classes(module_name):
    module = importlib.import_module(module_name)

    test_case_classes = []
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            test_case_classes.append(obj)

    return test_case_classes


def run_test_cases():
    # change this for the generated file that containing the test cases
    module_name = "test_app"

    test_case_classes = discover_test_case_classes(module_name)
    from test_app import MyTestCase

    cov = coverage.Coverage(omit=["*test_app.py"])
    cov.start()

    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))

    test_runner = unittest.TextTestRunner()
    test_result = test_runner.run(test_suite)

    valid_count = test_result.testsRun - len(test_result.errors)
    invalid_count = len(test_result.errors)

    print("Name\t\tValid\tFailed\tPercentage")
    print("------------------------------------------")
    print(
        "test_app\t{}\t{}\t{:.2f}%".format(
            valid_count, invalid_count, (valid_count / test_result.testsRun) * 100
        )
    )
    print("------------------------------------------")
    print()

    cov.stop()
    cov.save()
    cov.report()


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    run_test_cases()


if __name__ == "__main__":
    main()

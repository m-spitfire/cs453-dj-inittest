import unittest
import coverage
from django.test import TestCase
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


import django
django.setup()

import importlib

def discover_test_case_classes(module_name):
    module = importlib.import_module(module_name)

    test_case_classes = []
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
            test_case_classes.append(obj)

    return test_case_classes

def run_test_cases():
    module_name = "test_app" #change this for the generated file that containing the test cases

    test_case_classes = discover_test_case_classes(module_name)
    from test_app import MyTestCase
    cov = coverage.Coverage(omit=["*test_app.py"])
    # cov = coverage.Coverage()
    cov.start()

    test_suite = unittest.TestSuite()

    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))

    test_runner = unittest.TextTestRunner()
    test_result = test_runner.run(test_suite)

    valid_count = test_result.testsRun - len(test_result.errors)
    invalid_count = len(test_result.errors)

    # print("Valid test cases:", valid_count)
    # print("Invalid test cases:", invalid_count)
    # valid_percentage = valid_count / test_result.testsRun * 100
    # print("Percentage of valid test cases: {:.2f}%".format(valid_percentage))  

    print("Name\t\tValid\tFailed\tPercentage")
    print("------------------------------------------")
    print("test_app\t{}\t{}\t{:.2f}%".format(valid_count, invalid_count, (valid_count / test_result.testsRun) * 100))
    print("------------------------------------------")
    # print("Percentage of valid test cases:", valid_count/test_result.testsRun * 100)
    print()

    # for test_case_class in test_case_classes:
    #     valid_count = test_result.testsRun - len(test_result.failures) - len(test_result.errors)
    #     invalid_count = len(test_result.failures) + len(test_result.errors)

    #     print(f"Test case class: {test_case_class.__name__}")
    #     print("Valid test cases:", valid_count)
    #     print("Invalid test cases:", invalid_count)
    #     print("Percentage of valid test cases:", valid_count/test_result.testsRun * 100)
    #     print()

    cov.stop()
    cov.save()
    cov.report()


if __name__ == "__main__":
    run_test_cases()

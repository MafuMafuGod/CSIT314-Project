"""
TDD test runner

Instructions:
    python tdd_runner.py tests.test_tdd_31_validate_fields
It prints whether the test passed and the message of every failure
"""
import sys
import unittest

# the test module to run, e.g. tests.test_tdd_31_validate_fields
moduleName = sys.argv[1]

# load every test in that module
suite = unittest.defaultTestLoader.loadTestsFromName(moduleName)

# run the tests 
runner = unittest.TextTestRunner(stream=open("nul" if sys.platform == "win32" else "/dev/null", "w"))
result = runner.run(suite)

print("Is the test successful?:", result.wasSuccessful())
for test, message in result.failures + result.errors:
    # show only the last line of the message, e.g. "...expected:<['u']> but was:<[]>"
    print("Failure:", test.id().split(".")[-1], "-", message.strip().split("\n")[-1])
print(f"Tests run: {result.testsRun}, failed: {len(result.failures) + len(result.errors)}")

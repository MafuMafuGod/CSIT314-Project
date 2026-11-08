"""
TDD cycle 1: User Story #31 (Customer logs in) - validateFields(u, p)

Rule from the use case (alternate flow 5a): if the email or password is empty,
the page must tell the Customer which fields are missing.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boundary.user_login_page import validateFields         # the function we are testing


class ValidateFieldsTest(unittest.TestCase):
    longMessage = False          # show only our own failure message

    def testAllFieldsFilled(self):
        # both fields filled -> nothing is missing
        actual = validateFields("customer@4reno.com", "password123")
        self.assertEqual([], actual, f"All filled expected:<[]> but was:<{actual}>")

    def testEmailMissing(self):
        # empty email -> "u" (the username/email field) is missing
        actual = validateFields("", "password123")
        self.assertEqual(["u"], actual, f"Email missing expected:<['u']> but was:<{actual}>")

    def testPasswordMissing(self):
        # empty password -> "p" is missing
        actual = validateFields("customer@4reno.com", "")
        self.assertEqual(["p"], actual, f"Password missing expected:<['p']> but was:<{actual}>")

    def testBothMissing(self):
        # both empty -> both fields are missing, email first
        actual = validateFields("", "")
        self.assertEqual(["u", "p"], actual, f"Both missing expected:<['u', 'p']> but was:<{actual}>")


if __name__ == "__main__":
    unittest.main()

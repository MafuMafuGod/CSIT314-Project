"""
TDD cycle 1: User Story #31 (Customer logs in) - validateFields(u, p)

Cycle 1: validateFields(u, p)
    Rule (alternate flow 5a): if the email or password is empty, the page must tell the Customer which fields are missing.

Cycle 4: login credentials are case-sensitive
    Found by test case TC31-8: typing the email in capital letters (CUSTOMER@4RENO.COM) logged in,
    but the session then held the capital letters, so the Shortlist showed nothing.
    Rule: the email and the password must match the account exactly (case-sensitive), so
    CUSTOMER@4RENO.COM or PASSWORD123 is rejected, and the session always holds the stored email.

Run:   python tdd_runner.py tests.test_tdd_31_customer_login
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                        # the Flask app
from boundary.user_login_page import validateFields             # Cycle 1: function we are testing
from entity import UserAccount                                  # Cycle 4: Entity we are testing

# Cycle 1 
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

# Cycle 4
class CaseSensitiveLoginTest(unittest.TestCase):
    longMessage = False          # show only our own failure message

    def testExactCredentialsLogIn(self):
        actual = UserAccount.userAccountLogin("customer@4reno.com", "password123")
        self.assertEqual(True, actual, f"Exact credentials expected:<True> but was:<{actual}>")

    def testEmailInCapitalsIsRejected(self):
        actual = UserAccount.userAccountLogin("CUSTOMER@4RENO.COM", "password123")
        self.assertEqual(False, actual, f"Email in capitals expected:<False> but was:<{actual}>")

    def testPasswordInCapitalsIsRejected(self):
        actual = UserAccount.userAccountLogin("customer@4reno.com", "PASSWORD123")
        self.assertEqual(False, actual, f"Password in capitals expected:<False> but was:<{actual}>")

    def testSessionHoldsStoredEmailAfterLogin(self):
        # log in, then look at what the session remembers
        app_module.app.config["TESTING"] = True
        with app_module.app.test_client() as browser:
            with browser.session_transaction() as s:
                s["csrf"] = "t"
            browser.post("/login", data={"u": "customer@4reno.com", "p": "password123", "csrf_token": "t"})
            with browser.session_transaction() as s:
                actual = s.get("u")
        self.assertEqual("customer@4reno.com", actual,
                         f"Session email expected:<customer@4reno.com> but was:<{actual}>")

if __name__ == "__main__":
    unittest.main()

"""
TDD cycle 1: User Story #31 (Customer logs in) - validateFields(u, p)

Cycle 1: validateFields(u, p)
    Rule (alternate flow 5a): if the email or password is empty, the page must tell the Customer which fields are missing.

Cycle 4: the email kept in the session after login
    Bug found by test case TC31-8: if the Customer types the email in capital letters
    (CUSTOMER@4RENO.COM) the login works, but the session kept the capital letters.
    The Shortlist (and the designer's portfolio) look items up by the email as stored,
    so they showed nothing.
    Rule: after login the session holds the email exactly as it is stored in the account,
    whatever capital letters were typed.

Run:   python tdd_runner.py tests.test_tdd_31_customer_login
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                        # the Flask app
from boundary.user_login_page import validateFields             # Cycle 1: function we are testing
from control import UserLoginController                         # Cycle 4: Control we are testing

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
class LoginSessionEmailTest(unittest.TestCase):
    longMessage = False          # show only our own failure message

    def testStoredEmailIsReturnedForCapitalLetters(self):
        # the Control returns the email as stored, even if typed in capital letters
        actual = UserLoginController().getAccountEmail("CUSTOMER@4RENO.COM")
        self.assertEqual("customer@4reno.com", actual,
                         f"Stored email expected:<customer@4reno.com> but was:<{actual}>")

    def testUnknownEmailIsReturnedUnchanged(self):
        # no such account -> nothing to correct, the typed text comes back
        actual = UserLoginController().getAccountEmail("nobody@4reno.com")
        self.assertEqual("nobody@4reno.com", actual,
                         f"Unknown email expected:<nobody@4reno.com> but was:<{actual}>")

    def testSessionKeepsStoredEmailAfterLogin(self):
        # log in with capital letters, then look at what the session remembers
        app_module.app.config["TESTING"] = True
        with app_module.app.test_client() as browser:
            with browser.session_transaction() as s:
                s["csrf"] = "t"
            browser.post("/login", data={"u": "CUSTOMER@4RENO.COM", "p": "password123", "csrf_token": "t"})
            with browser.session_transaction() as s:
                actual = s.get("u")
        self.assertEqual("customer@4reno.com", actual,
                         f"Session email expected:<customer@4reno.com> but was:<{actual}>")

if __name__ == "__main__":
    unittest.main()

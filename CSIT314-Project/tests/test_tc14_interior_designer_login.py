"""TC14: Interior Designer logs in securely.

Place this file in the project's tests/ directory and run with:
    python -m unittest tests.test_tc14_interior_designer_login -v
"""
from tests.tc_helpers import *  # noqa: F401,F403 - shared app, browser, and reset helpers


class TestTC14InteriorDesignerLogin(BaseTest):
    def test_tc14_1_valid_credentials_log_in_as_designer(self):
        browser = newBrowser()
        html = postText(
            browser,
            "/login",
            u=DESIGNER,
            p=DESIGNER_PASSWORD,
        )

        self.assertIn("Logged in successfully as Interior Designer.", html)
        with browser.session_transaction() as session:
            self.assertEqual(session.get("u"), DESIGNER)
            self.assertEqual(session.get("profile"), "designer")
        self.assertIn("Company Profile", getText(browser, "/designer/company"))

    def test_tc14_2_invalid_password_does_not_authenticate(self):
        browser = newBrowser()
        html = postText(
            browser,
            "/login",
            u=DESIGNER,
            p="design1234",
        )

        self.assertIn("Invalid username or password", html)
        self.assertIn("Account Login", html)
        with browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))
            self.assertIsNone(session.get("profile"))

    def test_tc14_3_missing_password_is_rejected(self):
        browser = newBrowser()
        html = postText(browser, "/login", u=DESIGNER, p="")

        self.assertIn("Please enter your password.", html)
        self.assertIn("Account Login", html)
        with browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))


if __name__ == "__main__":
    import unittest

    unittest.main()

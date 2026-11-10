"""TC06: User Admin logs in with valid credentials.

Place this file in the project's tests/ directory and run with:
    python -m unittest tests.test_tc06_user_admin_login -v
"""
from tests.tc_helpers import *  # noqa: F401,F403 - shared app, browser, and reset helpers


ADMIN_EMAIL = "admin@4reno.com"
ADMIN_PASSWORD = "admin123"


class TestTC06UserAdminLogin(BaseTest):
    def test_tc06_01_valid_credentials_log_in_as_user_admin(self):
        browser = newBrowser()
        html = postText(
            browser,
            "/login",
            u=ADMIN_EMAIL,
            p=ADMIN_PASSWORD,
        )

        self.assertIn("Logged in successfully as User Admin.", html)
        with browser.session_transaction() as session:
            self.assertEqual(session.get("u"), ADMIN_EMAIL)
            self.assertEqual(session.get("profile"), "admin")

        # Confirm the authenticated admin can open a User Management page.
        response = browser.get("/admin/users", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Account Login", cleanText(response.get_data(as_text=True)))

    def test_tc06_02_invalid_password_is_rejected_and_cleared(self):
        browser = newBrowser()
        html = postText(
            browser,
            "/login",
            u=ADMIN_EMAIL,
            p="admin1234",
        )

        self.assertIn("Invalid username or password", html)
        self.assertIn(f'value="{ADMIN_EMAIL}"', html)
        self.assertNotIn("admin1234", html)
        with browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))
            self.assertIsNone(session.get("profile"))

    def test_tc06_03_missing_password_is_rejected(self):
        browser = newBrowser()
        html = postText(browser, "/login", u=ADMIN_EMAIL, p="")

        self.assertIn("Please enter your password.", html)
        self.assertIn(f'value="{ADMIN_EMAIL}"', html)
        with browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))
            self.assertIsNone(session.get("profile"))


if __name__ == "__main__":
    import unittest

    unittest.main()

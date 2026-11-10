"""TC07: User Admin logs out and returns to the login page.

Place this file in the project's tests/ directory and run with:
    python -m unittest tests.test_tc07_user_admin_logout -v
"""
from tests.tc_helpers import *  # noqa: F401,F403 - shared app, browser, and reset helpers


ADMIN_EMAIL = "admin@4reno.com"
ADMIN_PASSWORD = "admin123"


class TestTC07UserAdminLogout(BaseTest):
    def setUp(self):
        super().setUp()
        self.browser = login(ADMIN_EMAIL, ADMIN_PASSWORD)

    def test_tc07_01_logout_ends_session_and_displays_confirmation(self):
        html = postText(self.browser, "/logout")

        self.assertIn("You have been logged out", html)
        self.assertIn("Your session has ended.", html)
        self.assertIn("Please log in again to access account-only features.", html)
        self.assertIn('href="/login"', html)

        with self.browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))
            self.assertIsNone(session.get("profile"))

    def test_tc07_02_user_management_requires_login_after_logout(self):
        postText(self.browser, "/logout")
        response = self.browser.get("/admin/users", follow_redirects=True)
        html = cleanText(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Account Login", html)
        with self.browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))


if __name__ == "__main__":
    import unittest

    unittest.main()

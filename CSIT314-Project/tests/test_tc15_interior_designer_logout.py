"""TC15: Interior Designer logs out and the active session ends.

Place this file in the project's tests/ directory and run with:
    python -m unittest tests.test_tc15_interior_designer_logout -v
"""
from tests.tc_helpers import *  # noqa: F401,F403 - shared app, browser, and reset helpers


class TestTC15InteriorDesignerLogout(BaseTest):
    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)

    def test_tc15_1_logout_confirms_session_ended(self):
        html = postText(self.browser, "/logout")

        self.assertIn("You have been logged out", html)
        self.assertIn("Your session has ended.", html)
        self.assertIn("Please log in again to access account-only features.", html)

        with self.browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))
            self.assertIsNone(session.get("profile"))

    def test_tc15_2_protected_company_page_requires_login_after_logout(self):
        postText(self.browser, "/logout")
        response = self.browser.get("/designer/contact-info", follow_redirects=True)
        html = cleanText(response.get_data(as_text=True))

        self.assertIn("Account Login", html)
        with self.browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))


if __name__ == "__main__":
    import unittest

    unittest.main()

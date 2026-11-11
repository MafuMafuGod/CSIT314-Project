"""
TC70 - Platform Admin Logging In (User Story #70)
Precondition: the Platform Admin has a registered account.
Each test follows one row (test step) of Matthew's test case sheet (TC70).
Run:  python -m unittest tests.test_tc70_platform_admin_login -v
"""
from tests.tc_helpers import *

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"


class TC70(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = newBrowser()                          # not logged in yet

    def test_TC70_1(self):
        # Platform Admin enters email and password, clicks 'Log in'
        html = postText(self.browser, "/login", u=PLATFORM, p=PLATFORM_PASSWORD)
        self.assertIn("Logged in successfully as Platform Management.", html)
        with self.browser.session_transaction() as session:
            self.assertEqual(PLATFORM, session.get("u"))

    def test_TC70_2(self):
        # Platform Admin enters the wrong password and clicks 'Log in'
        html = postText(self.browser, "/login", u=PLATFORM, p="wrongpass")
        self.assertIn("Invalid username or password", html)
        with self.browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))

    def test_TC70_3(self):
        # Platform Admin leaves Email and Password empty and clicks 'Log in'
        html = postText(self.browser, "/login", u="", p="")
        self.assertIn("Please enter your email.", html)
        self.assertIn("Please enter your password.", html)


if __name__ == "__main__":
    unittest.main()

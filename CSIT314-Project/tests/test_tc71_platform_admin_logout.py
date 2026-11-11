"""
TC71 - Platform Admin Logging Out (User Story #71)
Precondition: the Platform Admin is logged in.
Each test follows one row (test step) of Matthew's test case sheet (TC71).
Run:  python -m unittest tests.test_tc71_platform_admin_logout -v
"""
from tests.tc_helpers import *

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"


class TC71(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def test_TC71_1(self):
        # Platform Admin clicks 'Log Out' in the navigation bar
        html = postText(self.browser, "/logout")
        self.assertIn("You have been logged out", html)
        with self.browser.session_transaction() as session:
            self.assertIsNone(session.get("u"))

    def test_TC71_2(self):
        # After the session has ended, Platform Admin tries to open 'Project Reports'
        self.browser.post("/logout")
        response = self.browser.get("/platform/reports/daily")
        self.assertEqual(302, response.status_code)
        self.assertIn("/login", response.headers["Location"])
        self.assertIn("Please log in as a Platform Administrator.", getText(self.browser, "/platform/reports/daily"))


if __name__ == "__main__":
    unittest.main()

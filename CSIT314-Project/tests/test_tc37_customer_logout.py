"""
TC37 - Customer Logging Out (User Story #37)
Precondition: Customer is logged in.
Run:  python -m unittest tests.test_tc37_customer_logout -v
"""
from tests.tc_helpers import *


class TC37(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login()       # precondition: Customer logged in

    def test_TC37_1_menu_shows_log_out(self):
        html = getText(self.browser, "/home")
        self.assertIn("Log out", html)
        self.assertNotIn("> Log in</a>", html)   # no "Log in" option

    def test_TC37_2_click_log_out(self):
        html = postText(self.browser, "/logout")
        self.assertIn("You have been logged out", html)
        self.assertIn("Your session has ended.", html)
        self.assertIn("Login", html)

    def test_TC37_3_shortlist_after_logout(self):
        postText(self.browser, "/logout")
        html = getText(self.browser, "/shortlist")
        self.assertIn("Please log in to use your Shortlist.", html)
        self.assertIn("Account Login", html)

    def test_TC37_4_login_button_goes_to_login_page(self):
        html = postText(self.browser, "/logout")
        self.assertIn('href="/login"', html)                     # the Login button
        self.assertIn("Account Login", getText(self.browser, "/login"))

    def test_TC37_5_session_already_expired(self):
        expired = newBrowser()                   # nobody is logged in
        html = postText(expired, "/logout")
        self.assertIn("Account Login", html)

    def test_TC37_6_logout_address_typed_in_browser(self):
        response = self.browser.get("/logout")   # typing the address = GET
        self.assertEqual(405, response.status_code)
        # the Customer is still logged in
        self.assertEqual(200, self.browser.get("/shortlist").status_code)


if __name__ == "__main__":
    unittest.main()

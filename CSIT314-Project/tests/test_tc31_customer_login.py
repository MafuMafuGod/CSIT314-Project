"""
TC31 - Customer Logging In (User Story #31)
Run:  python -m unittest tests.test_tc31_customer_login -v
"""
from tests.tc_helpers import *   # helpers + BaseTest


class TC31(BaseTest):

    def test_TC31_1_open_login_page(self):
        # Customer opens the Log in page
        html = getText(newBrowser(), "/login")
        self.assertIn("Account Login", html)
        self.assertIn('name="u"', html)          # Email field
        self.assertIn('name="p"', html)          # Password field
        self.assertIn("Log in", html)            # button

    def test_TC31_2_both_fields_empty(self):
        html = postText(newBrowser(), "/login", u="", p="")
        self.assertIn("Please enter your email.", html)
        self.assertIn("Please enter your password.", html)
        self.assertIn("Account Login", html)     # stays on the Log in page

    def test_TC31_3_email_empty(self):
        html = postText(newBrowser(), "/login", u="", p="password123")
        self.assertIn("Please enter your email.", html)
        self.assertNotIn("Please enter your password.", html)

    def test_TC31_4_password_empty(self):
        html = postText(newBrowser(), "/login", u="customer@4reno.com", p="")
        self.assertIn("Please enter your password.", html)
        self.assertNotIn("Please enter your email.", html)
        self.assertIn('value="customer@4reno.com"', html)    # email is kept

    def test_TC31_5_wrong_password(self):
        html = postText(newBrowser(), "/login", u="customer@4reno.com", p="wrongpass")
        self.assertIn("Invalid username or password", html)
        self.assertIn('value="customer@4reno.com"', html)    # email is kept
        self.assertNotIn("wrongpass", html)                  # password is cleared

    def test_TC31_6_email_not_registered(self):
        html = postText(newBrowser(), "/login", u="nobody@4reno.com", p="password123")
        self.assertIn("Invalid username or password", html)

    def test_TC31_7_login_success(self):
        html = postText(newBrowser(), "/login", u="customer@4reno.com", p="password123")
        self.assertIn("Logged in successfully as Customer.", html)
        self.assertIn("My Shortlist", html)
        self.assertIn("Log out", html)

    def test_TC31_8_email_in_capital_letters(self):
        browser = newBrowser()
        browser.post("/login", data={"u": "CUSTOMER@4RENO.COM", "p": "password123", "csrf_token": "t"})
        # the session must hold the email as stored (small letters)
        with browser.session_transaction() as s:
            self.assertEqual("customer@4reno.com", s.get("u"))
        # so My Shortlist still shows the Customer's saved IDPs
        html = getText(browser, "/shortlist")
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertIn("Sengkang BTO Minimalist Living Room", html)


if __name__ == "__main__":
    unittest.main()

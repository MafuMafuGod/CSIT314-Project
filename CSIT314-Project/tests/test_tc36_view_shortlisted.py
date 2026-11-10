"""
TC36 - Customer Viewing a Project from the Shortlist (User Story #36)
Precondition: Customer is logged in. The Shortlist has 2 IDPs (ids 2 and 4).
Run:  python -m unittest tests.test_tc36_view_shortlisted -v
"""
from tests.tc_helpers import *


class TC36(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login()       # precondition: Customer logged in

    def test_TC36_1_view_saved_project(self):
        html = getText(self.browser, "/shortlist/2")
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertIn("Kitchen", html)
        self.assertIn("Open kitchen with a quartz island", html)
        self.assertIn("Back to Shortlist", html)

    def test_TC36_2_back_to_shortlist(self):
        html = getText(self.browser, "/shortlist/2")
        self.assertIn('href="/shortlist"', html)                 # the Back button link
        shortlist = getText(self.browser, "/shortlist")          # clicking it
        self.assertIn("Punggol Waterway Condo Kitchen", shortlist)
        self.assertIn("Sengkang BTO Minimalist Living Room", shortlist)

    def test_TC36_3_idp_not_in_shortlist(self):
        html = getText(self.browser, "/shortlist/1")             # Tampines (not saved)
        self.assertIn("This project is not in your Shortlist.", html)
        self.assertIn("Back to Shortlist", html)

    def test_TC36_4_saved_idp_was_removed(self):
        removeIDP(4)
        html = getText(self.browser, "/shortlist/4")
        self.assertIn("This project is no longer available.", html)
        self.assertIn("Back to Shortlist", html)

    def test_TC36_5_visitor_not_logged_in(self):
        html = getText(newBrowser(), "/shortlist/2")
        self.assertIn("Please log in to use your Shortlist.", html)
        self.assertIn("Account Login", html)

    def test_TC36_6_designer_cannot_open(self):
        designer = login(DESIGNER, DESIGNER_PASSWORD)
        html = getText(designer, "/shortlist/2")
        self.assertIn("Only Customers have a Shortlist.", html)

    def test_TC36_7_address_has_letters(self):
        response = self.browser.get("/shortlist/abc")
        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    unittest.main()

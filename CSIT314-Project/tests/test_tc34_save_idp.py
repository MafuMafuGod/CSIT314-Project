"""
TC34 - Customer Saving an IDP to the Shortlist (User Story #34)
Precondition: Customer is logged in. The Shortlist already has 2 IDPs (ids 2 and 4).
Run:  python -m unittest tests.test_tc34_save_idp -v
"""
from tests.tc_helpers import *


class TC34(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login()       # precondition: Customer logged in

    def test_TC34_1_save_idp(self):
        before = getIDP(5)._shortlistCount                       # 2
        html = postText(self.browser, "/idp/5/save")
        self.assertIn("IDP saved to your favourite list.", html)
        self.assertEqual(before + 1, getIDP(5)._shortlistCount)  # 2 -> 3

    def test_TC34_2_shortlist_shows_3_idps(self):
        postText(self.browser, "/idp/5/save")
        html = getText(self.browser, "/shortlist")
        self.assertIn("3 saved projects", html)
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertIn("Sengkang BTO Minimalist Living Room", html)
        self.assertIn("Clementi Resale Japandi Bedroom", html)

    def test_TC34_3_save_same_idp_again(self):
        postText(self.browser, "/idp/5/save")
        countAfterFirstSave = getIDP(5)._shortlistCount
        html = postText(self.browser, "/idp/5/save")
        self.assertIn("This IDP is already in your favourite list.", html)
        self.assertEqual(countAfterFirstSave, getIDP(5)._shortlistCount)   # no change
        self.assertEqual(3, len(Shortlist.getSavedIDPIDs(CUSTOMER)))        # not saved twice

    def test_TC34_4_idp_removed_before_saving(self):
        removeIDP(3)                                             # Bishan Landed Home Revamp
        html = postText(self.browser, "/idp/3/save")
        self.assertIn("This IDP could not be saved. Please try again.", html)
        self.assertEqual(2, len(Shortlist.getSavedIDPIDs(CUSTOMER)))        # nothing added

    def test_TC34_5_visitor_not_logged_in(self):
        html = postText(newBrowser(), "/idp/5/save")
        self.assertIn("Please log in to use your Shortlist.", html)
        self.assertIn("Account Login", html)

    def test_TC34_6_designer_cannot_save(self):
        designer = login(DESIGNER, DESIGNER_PASSWORD)
        html = postText(designer, "/idp/5/save")
        self.assertIn("Only Customers have a Shortlist.", html)


if __name__ == "__main__":
    unittest.main()

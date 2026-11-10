"""
TC35 - Customer Searching the Shortlist (User Story #35)
Precondition: Customer is logged in. Shortlist has 2 IDPs:
Punggol Waterway Condo Kitchen and Sengkang BTO Minimalist Living Room.
Run:  python -m unittest tests.test_tc35_search_shortlist -v
"""
from tests.tc_helpers import *


class TC35(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login()       # precondition: Customer logged in

    def test_TC35_1_open_shortlist(self):
        html = getText(self.browser, "/shortlist")
        self.assertIn("Search saved projects", html)
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertIn("Sengkang BTO Minimalist Living Room", html)

    def test_TC35_2_empty_keyword(self):
        html = getText(self.browser, "/shortlist?keyword=")
        self.assertIn("Please enter a keyword to search your Shortlist.", html)

    def test_TC35_3_keyword_kitchen(self):
        html = getText(self.browser, "/shortlist?keyword=kitchen")
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertNotIn("Sengkang BTO Minimalist Living Room", html)

    def test_TC35_4_only_own_saved_idps_are_searched(self):
        html = getText(self.browser, "/shortlist?keyword=living")
        self.assertIn("Sengkang BTO Minimalist Living Room", html)
        self.assertNotIn("Tampines HDB Scandinavian Makeover", html)   # not saved

    def test_TC35_5_no_match(self):
        html = getText(self.browser, "/shortlist?keyword=bedroom")
        self.assertIn("No matching saved projects were found.", html)

    def test_TC35_6_keyword_too_long(self):
        html = getText(self.browser, "/shortlist?keyword=" + "a" * 101)
        self.assertIn("Keyword must be 100 characters or fewer.", html)

    def test_TC35_7_shortlist_is_empty(self):
        # a new Customer who has saved nothing
        UserAccount.createAccount("New Customer", "newcustomer@4reno.com", "password123", "customer")
        newCustomer = login("newcustomer@4reno.com", "password123")
        html = getText(newCustomer, "/shortlist?keyword=kitchen")
        self.assertIn("Your Shortlist is empty. Save projects from Search IDPs to see them here.", html)
        self.assertIn("Browse IDPs", html)

    def test_TC35_8_removed_idp_is_left_out(self):
        removeIDP(4)                                             # Sengkang BTO Minimalist Living Room
        html = getText(self.browser, "/shortlist")
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertNotIn("Sengkang BTO Minimalist Living Room", html)


if __name__ == "__main__":
    unittest.main()

"""
TC41 - Interior Designer Viewing IDP Shortlist Counts (User Story #41)
Precondition: the Interior Designer is logged in, has created at least one IDP and is on the dashboard. Customer shortlists have been recorded.
Each test follows one row (test step) of Matthew's test case sheet (TC41).
Run:  python -m unittest tests.test_tc41_view_idp_shortlist_counts -v
"""
from tests.tc_helpers import *

NEW_DESIGNER = "newid@4reno.com"
NEW_DESIGNER_PASSWORD = "newid123"


class TC41(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in with IDPs

    def test_TC41_1(self):
        # ID clicks 'IDP Interest', then the 'Shortlisted' tab
        html = getText(self.browser, "/designer/interest/shortlists")
        rows = InteriorDesignProject.getShortlistCounts(DESIGNER)
        self.assertEqual(5, len(rows))
        self.assertEqual(sorted([r["shortlistCount"] for r in rows], reverse=True), [r["shortlistCount"] for r in rows])
        self.assertEqual("Punggol Waterway Condo Kitchen", rows[0]["title"])
        self.assertIn("77", html)

    def test_TC41_2(self):
        # Customer saves an IDP to their shortlist, then ID opens the 'Shortlisted' tab
        self.assertEqual(2, getIDP(5)._shortlistCount)
        login(CUSTOMER, CUSTOMER_PASSWORD).post("/idp/5/save", follow_redirects=True)
        self.assertEqual(3, getIDP(5)._shortlistCount)

    def test_TC41_3(self):
        # Customer saves the same IDP again, then ID opens the 'Shortlisted' tab
        customer = login(CUSTOMER, CUSTOMER_PASSWORD)
        customer.post("/idp/5/save", follow_redirects=True)
        html = postText(customer, "/idp/5/save")
        self.assertIn("This IDP is already in your favourite list.", html)
        self.assertEqual(3, getIDP(5)._shortlistCount)

    def test_TC41_4(self):
        # ID with no IDPs clicks 'IDP Interest', then the 'Shortlisted' tab
        UserAccount.createAccount("New Designer", NEW_DESIGNER, NEW_DESIGNER_PASSWORD, "designer")
        html = getText(login(NEW_DESIGNER, NEW_DESIGNER_PASSWORD), "/designer/interest/shortlists")
        self.assertIn("No IDP found", html)
        self.assertIn("Create IDP", html)


if __name__ == "__main__":
    unittest.main()

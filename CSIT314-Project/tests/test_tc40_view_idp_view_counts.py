"""
TC40 - Interior Designer Viewing IDP View Counts (User Story #40)
Precondition: the Interior Designer is logged in, has created at least one IDP and is on the dashboard.
Each test follows one row (test step) of Matthew's test case sheet (TC40).
Run:  python -m unittest tests.test_tc40_view_idp_view_counts -v
"""
from tests.tc_helpers import *

NEW_DESIGNER = "newid@4reno.com"
NEW_DESIGNER_PASSWORD = "newid123"


class TC40(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in with IDPs

    def test_TC40_1(self):
        # ID clicks 'IDP Interest' in the navigation bar
        html = getText(self.browser, "/designer/interest/views")
        rows = InteriorDesignProject.getViewCounts(DESIGNER)
        self.assertEqual(5, len(rows))
        self.assertEqual(sorted([r["viewCount"] for r in rows], reverse=True), [r["viewCount"] for r in rows])
        self.assertEqual("Punggol Waterway Condo Kitchen", rows[0]["title"])
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertIn("518", html)

    def test_TC40_2(self):
        # Customer opens the details page of an IDP, then ID clicks 'IDP Interest'
        self.assertEqual(23, getIDP(5)._viewCount)
        login(CUSTOMER, CUSTOMER_PASSWORD).get("/idp/5")
        self.assertEqual(24, getIDP(5)._viewCount)
        self.assertIn("24", getText(self.browser, "/designer/interest/views"))

    def test_TC40_3(self):
        # ID with no IDPs clicks 'IDP Interest' in the navigation bar
        UserAccount.createAccount("New Designer", NEW_DESIGNER, NEW_DESIGNER_PASSWORD, "designer")
        html = getText(login(NEW_DESIGNER, NEW_DESIGNER_PASSWORD), "/designer/interest/views")
        self.assertIn("No IDP found", html)
        self.assertIn("Create IDP", html)


if __name__ == "__main__":
    unittest.main()

"""
TC61 - Interior Designer Searching the Portfolio of Past Projects (User Story #61)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc61_search_past_portfolio -v
"""
from tests.tc_helpers import *


class TC61(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC61_1(self):
        # ID enters a keyword in the search bar and clicks 'Search'
        html = getText(self.browser, "/designer/portfolio?kind=past&q=kitchen")
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertNotIn("Bishan Landed Home Revamp", html)

    def test_TC61_2(self):
        # ID enters a keyword that matches nothing and clicks 'Search'
        html = getText(self.browser, "/designer/portfolio?kind=past&q=zzz")
        self.assertIn("No matching results were found", html)
        self.assertIn('name="q"', html)

    def test_TC61_3(self):
        # ID enters a keyword longer than 100 characters and clicks 'Search'
        html = getText(self.browser, "/designer/portfolio?kind=past&q=" + "x" * 101)
        self.assertIn("Keyword must be 100 characters or fewer.", html)


if __name__ == "__main__":
    unittest.main()

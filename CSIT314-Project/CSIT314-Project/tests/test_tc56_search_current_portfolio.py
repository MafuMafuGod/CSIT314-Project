"""
TC56 - Interior Designer Searching the Portfolio of Current Projects (User Story #56)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc56_search_current_portfolio -v
"""
from tests.tc_helpers import *


class TC56(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC56_1(self):
        # ID clicks 'Search'
        html = getText(self.browser, "/designer/portfolio?kind=current&q=minimalist")
        self.assertIn("Sengkang BTO Minimalist Living Room", html)
        self.assertNotIn("Clementi Resale Japandi Bedroom", html)

    def test_TC56_2(self):
        # ID clicks 'Search'
        html = getText(self.browser, "/designer/portfolio?kind=current&q=zzz")
        self.assertIn("No matching results were found", html)
        self.assertIn('name="q"', html)

    def test_TC56_3(self):
        # ID clicks 'Search'
        html = getText(self.browser, "/designer/portfolio?kind=current&q=" + "x" * 101)
        self.assertIn("Keyword must be 100 characters or fewer.", html)


if __name__ == "__main__":
    unittest.main()

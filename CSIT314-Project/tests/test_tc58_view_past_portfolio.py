"""
TC58 - Interior Designer Viewing the Portfolio of a Past Project (User Story #58)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc58_view_past_portfolio -v
"""
from tests.tc_helpers import *


class TC58(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC58_1(self):
        # ID selects a past project
        html = getText(self.browser, "/designer/portfolio/past/1")
        for text in ("Tampines HDB Scandinavian Makeover", "Light oak floors", "Scandinavian, open-plan living and dining",
                     "Completion date", "2026-08-10"):
            self.assertIn(text, html)

    def test_TC58_2(self):
        # ID selects a past project whose information cannot be retrieved
        removeIDP(1)
        html = getText(self.browser, "/designer/portfolio/past/1")
        self.assertIn("This project&#39;s portfolio information is unavailable.", html)
        self.assertIn("Back to portfolio", html)


if __name__ == "__main__":
    unittest.main()

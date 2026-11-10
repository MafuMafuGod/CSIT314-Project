"""
TC53 - Interior Designer Viewing the Portfolio of a Current Project (User Story #53)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc53_view_current_portfolio -v
"""
from tests.tc_helpers import *


class TC53(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC53_1(self):
        # ID selects a current project
        html = getText(self.browser, "/designer/portfolio")
        self.assertIn("Sengkang BTO Minimalist Living Room", html)
        html = getText(self.browser, "/designer/portfolio/current/4")
        for text in ("Sengkang BTO Minimalist Living Room", "Minimalist living room with built-in TV console",
                     "Minimalist, hidden storage, neutral palette", "Matte laminate, fluted glass, beige microcement", "Current"):
            self.assertIn(text, html)

    def test_TC53_2(self):
        # ID selects a current project whose information cannot be retrieved (it is no longer in the portfolio)
        removeIDP(4)
        html = getText(self.browser, "/designer/portfolio/current/4")
        self.assertIn("This project&#39;s portfolio information is unavailable.", html)
        self.assertIn("Back to portfolio", html)


if __name__ == "__main__":
    unittest.main()

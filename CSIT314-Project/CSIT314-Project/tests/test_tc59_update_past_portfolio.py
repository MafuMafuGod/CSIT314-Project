"""
TC59 - Interior Designer Updating the Portfolio of a Past Project (User Story #59)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc59_update_past_portfolio -v
"""
from tests.tc_helpers import *


class TC59(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC59_1(self):
        # ID changes the materials and clicks 'Save'
        html = getText(self.browser, "/designer/portfolio/past/1/edit")
        self.assertIn('value="Tampines HDB Scandinavian Makeover"', html)
        html = postText(self.browser, "/designer/portfolio/past/1/edit", title="Tampines HDB Scandinavian Makeover",
                        description="Light oak floors", designs="Scandinavian", materials="Oak veneer, white quartz",
                        category="Living Room", completionDate="2026-08-10")
        self.assertIn("Portfolio updated successfully.", html)
        self.assertIn("Oak veneer, white quartz", html)

    def test_TC59_2(self):
        # ID enters a completion date in the future and clicks 'Save'
        html = postText(self.browser, "/designer/portfolio/past/1/edit", title="Tampines HDB Scandinavian Makeover",
                        description="Light oak floors", designs="Scandinavian", materials="Oak veneer",
                        category="Living Room", completionDate="2099-12-25")
        self.assertIn("The completion date cannot be in the future.", html)
        self.assertEqual("2026-08-10", getIDP(1)._completionDate)

    def test_TC59_3(self):
        # ID clicks 'Save'
        getText(self.browser, "/designer/portfolio/past/1/edit")
        removeIDP(1)
        html = postText(self.browser, "/designer/portfolio/past/1/edit", title="Tampines HDB Scandinavian Makeover",
                        description="Light oak floors", designs="Scandinavian", materials="Oak veneer",
                        category="Living Room", completionDate="2026-08-10")
        self.assertIn("The changes could not be saved. Please try again.", html)


if __name__ == "__main__":
    unittest.main()

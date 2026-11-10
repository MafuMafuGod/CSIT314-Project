"""
TC60 - Interior Designer Deleting the Portfolio of a Past Project (User Story #60)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc60_delete_past_portfolio -v
"""
from tests.tc_helpers import *


class TC60(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC60_1(self):
        # ID clicks 'Delete project'
        html = postText(self.browser, "/designer/portfolio/past/1/delete")
        self.assertIn("The project was deleted from your portfolio.", html)
        self.assertNotIn("Tampines HDB Scandinavian Makeover", html)
        self.assertIsNone(getIDP(1))

    def test_TC60_2(self):
        # ID clicks 'Cancel'
        html = getText(self.browser, "/designer/portfolio?kind=past")
        self.assertIn('id="delete-1"', html)
        self.assertIn('href="#">Cancel</a>', html)
        self.assertIn("Tampines HDB Scandinavian Makeover", getText(self.browser, "/designer/portfolio?kind=past"))
        self.assertIsNotNone(getIDP(1))

    def test_TC60_3(self):
        # The project can no longer be found, so the deletion fails
        removeIDP(1)
        html = postText(self.browser, "/designer/portfolio/past/1/delete")
        self.assertIn("The project could not be deleted. Please try again.", html)
        self.assertIn("My Portfolio", html)


if __name__ == "__main__":
    unittest.main()

"""
TC55 - Interior Designer Deleting the Portfolio of a Current Project (User Story #55)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc55_delete_current_portfolio -v
"""
from tests.tc_helpers import *


class TC55(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC55_1(self):
        # ID clicks 'Delete project'
        html = postText(self.browser, "/designer/portfolio/current/4/delete")
        self.assertIn("The project was deleted from your portfolio.", html)
        self.assertNotIn("Sengkang BTO Minimalist Living Room", html)
        self.assertIsNone(getIDP(4))

    def test_TC55_2(self):
        # ID clicks 'Cancel'
        html = getText(self.browser, "/designer/portfolio")
        self.assertIn('id="delete-4"', html)               # the confirmation pop-up
        self.assertIn('href="#">Cancel</a>', html)          # Cancel only closes it (sends nothing)
        self.assertIn("Sengkang BTO Minimalist Living Room", getText(self.browser, "/designer/portfolio"))
        self.assertIsNotNone(getIDP(4))

    def test_TC55_3(self):
        # The project can no longer be found, so the deletion fails
        removeIDP(4)
        html = postText(self.browser, "/designer/portfolio/current/4/delete")
        self.assertIn("The project could not be deleted. Please try again.", html)
        self.assertIn("My Portfolio", html)


if __name__ == "__main__":
    unittest.main()

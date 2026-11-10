"""
TC54 - Interior Designer Updating the Portfolio of a Current Project (User Story #54)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc54_update_current_portfolio -v
"""
from tests.tc_helpers import *


class TC54(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC54_1(self):
        # ID changes the title and clicks 'Save'
        html = getText(self.browser, "/designer/portfolio/current/4/edit")
        self.assertIn('value="Sengkang BTO Minimalist Living Room"', html)
        html = postText(self.browser, "/designer/portfolio/current/4/edit", title="Sengkang BTO Living Room (revised)",
                        description="Minimalist living room", designs="Minimalist", materials="Laminate", category="Living Room")
        self.assertIn("Portfolio updated successfully.", html)
        self.assertIn("Sengkang BTO Living Room (revised)", html)

    def test_TC54_2(self):
        # ID clears the title and clicks 'Save'
        html = postText(self.browser, "/designer/portfolio/current/4/edit", title="",
                        description="Minimalist living room", designs="Minimalist", materials="Laminate", category="Living Room")
        self.assertIn("Please correct the highlighted fields.", html)
        self.assertIn("Please enter a project title.", html)
        self.assertEqual("Sengkang BTO Minimalist Living Room", getIDP(4)._title)

    def test_TC54_3(self):
        # ID clicks 'Save'
        getText(self.browser, "/designer/portfolio/current/4/edit")
        removeIDP(4)
        html = postText(self.browser, "/designer/portfolio/current/4/edit", title="Sengkang BTO Living Room (revised)",
                        description="Minimalist living room", designs="Minimalist", materials="Laminate", category="Living Room")
        self.assertIn("The changes could not be saved. Please try again.", html)


if __name__ == "__main__":
    unittest.main()

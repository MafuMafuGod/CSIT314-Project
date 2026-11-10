"""
TC57 - Interior Designer Creating a Portfolio for a Past Project (User Story #57)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc57_create_past_portfolio -v
"""
from tests.tc_helpers import *


class TC57(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC57_1(self):
        # ID enters the project details and completion date and clicks 'Create Portfolio'
        html = postText(self.browser, "/designer/portfolio/create/past", title="Toa Payoh HDB Kitchen Refresh", description="Refreshed kitchen with new cabinets", designs="Retro-modern, two-tone cabinets", materials="Laminate, subway tiles", category="Kitchen", completionDate="2026-10-30")
        self.assertIn("Portfolio for your past project was created successfully.", html)
        self.assertIn("Toa Payoh HDB Kitchen Refresh", html)
        self.assertIn("Past", [i._status for i in InteriorDesignProject._idps if i._title == "Toa Payoh HDB Kitchen Refresh"])

    def test_TC57_2(self):
        # ID leaves the required fields blank and clicks 'Create Portfolio'
        before = len(InteriorDesignProject._idps)
        html = postText(self.browser, "/designer/portfolio/create/past", title="", description="", designs="", materials="", category="", completionDate="")
        for message in ("Please correct the highlighted fields.", "Please enter a project title.", "Please enter a project description.", "Please describe the designs.", "Please list the materials.", "Please enter the completion date."):
            self.assertIn(message, html)
        self.assertEqual(before, len(InteriorDesignProject._idps))

    def test_TC57_3(self):
        # ID enters a completion date in the future and clicks 'Create Portfolio'
        before = len(InteriorDesignProject._idps)
        html = postText(self.browser, "/designer/portfolio/create/past", title="Toa Payoh HDB Kitchen Refresh", description="Refreshed kitchen with new cabinets", designs="Retro-modern, two-tone cabinets", materials="Laminate, subway tiles", category="Kitchen", completionDate="2099-12-25")
        self.assertIn("The completion date cannot be in the future.", html)
        self.assertEqual(before, len(InteriorDesignProject._idps))


if __name__ == "__main__":
    unittest.main()

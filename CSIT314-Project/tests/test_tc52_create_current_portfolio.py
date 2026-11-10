"""
TC52 - Interior Designer Creating a Portfolio for a Current Project (User Story #52)
Precondition: the Interior Designer is logged in and on the portfolio management page.
Each test follows one row (test step) of Test_Cases_52-61.xlsx.
Run:  python -m unittest tests.test_tc52_create_current_portfolio -v
"""
from tests.tc_helpers import *


class TC52(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in

    def test_TC52_1(self):
        # ID enters the project details and clicks 'Create Portfolio'
        html = postText(self.browser, "/designer/portfolio/create/current", title="Bedok Condo Study Nook", description="Compact study corner with built-in desk", designs="Warm minimalist, wall-mounted desk", materials="Walnut veneer, matte black steel", category="Study")
        self.assertIn("Portfolio for your current project was created successfully.", html)
        self.assertIn("Bedok Condo Study Nook", html)
        self.assertIn("Current", [i._status for i in InteriorDesignProject._idps if i._title == "Bedok Condo Study Nook"])

    def test_TC52_2(self):
        # ID leaves the required fields blank and clicks 'Create Portfolio'
        before = len(InteriorDesignProject._idps)
        html = postText(self.browser, "/designer/portfolio/create/current", title="", description="", designs="", materials="", category="")
        for message in ("Please correct the highlighted fields.", "Please enter a project title.", "Please enter a project description.", "Please describe the designs.", "Please list the materials."):
            self.assertIn(message, html)
        self.assertEqual(before, len(InteriorDesignProject._idps))


if __name__ == "__main__":
    unittest.main()

"""
TC10 - Interior Designer Viewing a Company Profile (User Story #10)
Precondition: the Interior Designer is logged in and has a company profile.
Each test follows one row (test step) of Matthew's test case sheet (TC10).
Run:  python -m unittest tests.test_tc10_view_company_profile -v
"""
import copy
from tests.tc_helpers import *
from entity import CompanyProfile

NEW_DESIGNER = "newid@4reno.com"
NEW_DESIGNER_PASSWORD = "newid123"


class TC10(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedProfiles = copy.deepcopy(CompanyProfile._profiles)
        CompanyProfile.createProfile(DESIGNER, "Tristen Interiors", "HDB and condo renovations with a focus on storage.",
                                     "hello@tristeninteriors.sg", "61234567", "1 Sengkang Square, Singapore 545078",
                                     "https://www.tristeninteriors.sg")      # precondition: profile exists
        UserAccount.createAccount("New Designer", NEW_DESIGNER, NEW_DESIGNER_PASSWORD, "designer")
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)

    def tearDown(self):
        CompanyProfile._profiles = self.savedProfiles
        super().tearDown()

    def test_TC10_1(self):
        # ID clicks 'Company Profile', then 'View Company Profile'
        html = getText(self.browser, "/designer/company")
        for detail in ("Tristen Interiors", "HDB and condo renovations with a focus on storage.",
                       "hello@tristeninteriors.sg", "61234567", "1 Sengkang Square, Singapore 545078"):
            self.assertIn(detail, html)

    def test_TC10_2(self):
        # ID with no company profile clicks 'View Company Profile'
        html = getText(login(NEW_DESIGNER, NEW_DESIGNER_PASSWORD), "/designer/company")
        self.assertIn("Your company profile has not been created.", html)
        self.assertIn("Create Company Profile", html)


if __name__ == "__main__":
    unittest.main()

"""
TC9 - Interior Designer Creating a Company Profile (User Story #9)
Precondition: the Interior Designer is logged in and does not have a company profile yet.
Each test follows one row (test step) of Matthew's test case sheet (TC9).
Run:  python -m unittest tests.test_tc09_create_company_profile -v
"""
import copy
from tests.tc_helpers import *
from entity import CompanyProfile

PROFILE = dict(companyName="Tristen Interiors", description="HDB and condo renovations with a focus on storage.",
               businessEmail="hello@tristeninteriors.sg", businessPhone="61234567",
               businessAddress="1 Sengkang Square, Singapore 545078", website="https://www.tristeninteriors.sg")


class TC9(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedProfiles = copy.deepcopy(CompanyProfile._profiles)
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)    # precondition: ID logged in, no profile yet

    def tearDown(self):
        CompanyProfile._profiles = self.savedProfiles
        super().tearDown()

    def test_TC9_1(self):
        # ID fills in all fields and clicks 'Save'
        html = postText(self.browser, "/designer/company/create", **PROFILE)
        self.assertIn("Company profile created successfully.", html)
        self.assertIn("Tristen Interiors", html)
        self.assertTrue(CompanyProfile.profileExists(DESIGNER))

    def test_TC9_2(self):
        # ID leaves the company name empty and clicks 'Save'
        html = postText(self.browser, "/designer/company/create", **{**PROFILE, "companyName": ""})
        self.assertIn("Please correct the highlighted fields.", html)
        self.assertIn("Please enter your company name.", html)
        self.assertFalse(CompanyProfile.profileExists(DESIGNER))

    def test_TC9_3(self):
        # ID enters an invalid business email and clicks 'Save'
        html = postText(self.browser, "/designer/company/create", **{**PROFILE, "businessEmail": "hello-at-tristen"})
        self.assertIn("Please enter a valid email address.", html)
        self.assertFalse(CompanyProfile.profileExists(DESIGNER))

    def test_TC9_4(self):
        # ID enters a website without http:// or https:// and clicks 'Save'
        html = postText(self.browser, "/designer/company/create", **{**PROFILE, "website": "www.tristeninteriors.sg"})
        self.assertIn("Website must start with http:// or https://", html)
        self.assertFalse(CompanyProfile.profileExists(DESIGNER))

    def test_TC9_5(self):
        # ID who already has a company profile clicks 'Create Company Profile'
        postText(self.browser, "/designer/company/create", **PROFILE)
        html = getText(self.browser, "/designer/company/create")
        self.assertIn("You already have a company profile. Use Update to change it.", html)
        self.assertEqual(1, len([p for p in CompanyProfile._profiles if p._designerU == DESIGNER]))


if __name__ == "__main__":
    unittest.main()

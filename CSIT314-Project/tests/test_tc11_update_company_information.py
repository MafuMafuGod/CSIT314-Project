"""
TC11 - Interior Designer Updating Company Information (User Story #11)
Precondition: the Interior Designer is logged in and has a company profile.
Each test follows one row (test step) of Matthew's test case sheet (TC11).
Run:  python -m unittest tests.test_tc11_update_company_information -v
"""
import copy
from tests.tc_helpers import *
from entity import CompanyProfile

PROFILE = dict(companyName="Tristen Interiors", description="HDB and condo renovations with a focus on storage.",
               businessEmail="hello@tristeninteriors.sg", businessPhone="61234567",
               businessAddress="1 Sengkang Square, Singapore 545078", website="https://www.tristeninteriors.sg")


class TC11(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedProfiles = copy.deepcopy(CompanyProfile._profiles)
        CompanyProfile.createProfile(DESIGNER, *PROFILE.values())     # precondition: profile exists
        self.browser = login(DESIGNER, DESIGNER_PASSWORD)

    def tearDown(self):
        CompanyProfile._profiles = self.savedProfiles
        super().tearDown()

    def test_TC11_1(self):
        # ID clicks 'Company Profile', then 'Update Company Information'
        html = getText(self.browser, "/designer/company/update")
        self.assertIn('value="Tristen Interiors"', html)
        self.assertIn('value="hello@tristeninteriors.sg"', html)

    def test_TC11_2(self):
        # ID changes the description and clicks 'Save'
        newDescription = "HDB, condo and landed renovations with a focus on storage."
        html = postText(self.browser, "/designer/company/update", **{**PROFILE, "description": newDescription})
        self.assertIn("Company information updated successfully.", html)
        self.assertIn(newDescription, html)
        self.assertEqual(newDescription, CompanyProfile.getProfile(DESIGNER)["description"])

    def test_TC11_3(self):
        # ID clears the company name and clicks 'Save'
        html = postText(self.browser, "/designer/company/update", **{**PROFILE, "companyName": ""})
        self.assertIn("Please correct the highlighted fields.", html)
        self.assertIn("Please enter your company name.", html)
        self.assertEqual("Tristen Interiors", CompanyProfile.getProfile(DESIGNER)["companyName"])

    def test_TC11_4(self):
        # ID enters a phone number that is too short and clicks 'Save'
        html = postText(self.browser, "/designer/company/update", **{**PROFILE, "businessPhone": "123"})
        self.assertIn("Please enter a valid phone number (at least 8 digits).", html)
        self.assertEqual("61234567", CompanyProfile.getProfile(DESIGNER)["businessPhone"])


if __name__ == "__main__":
    unittest.main()

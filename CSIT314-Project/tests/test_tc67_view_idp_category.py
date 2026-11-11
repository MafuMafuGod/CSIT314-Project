"""
TC67 - Platform Admin Viewing an IDP Category (User Story #67)
Precondition: the Platform Admin is logged in and categories exist.
Each test follows one row (test step) of Matthew's test case sheet (TC67).
Run:  python -m unittest tests.test_tc67_view_idp_category -v
"""
import copy
from tests.tc_helpers import *
from entity import IDPCategory

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"


def categoryNames():
    return [c._name for c in IDPCategory._categories]

KITCHEN = "IDP-CAT-002"
STUDY = "IDP-CAT-004"

class TC67(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedCategories = copy.deepcopy(IDPCategory._categories)
        self.savedNextID = IDPCategory._nextID
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        IDPCategory._categories = self.savedCategories
        IDPCategory._nextID = self.savedNextID
        super().tearDown()

    def test_TC67_1(self):
        # Platform Admin clicks 'IDP Categories' and selects a category
        html = getText(self.browser, f"/platform/idp-categories/{KITCHEN}")
        self.assertIn("Kitchens, pantries and dining areas", html)
        self.assertIn("Punggol Waterway Condo Kitchen", html)

    def test_TC67_2(self):
        # Platform Admin selects a category that has no projects
        html = getText(self.browser, f"/platform/idp-categories/{STUDY}")
        self.assertIn("No projects are linked to this category yet.", html)


if __name__ == "__main__":
    unittest.main()

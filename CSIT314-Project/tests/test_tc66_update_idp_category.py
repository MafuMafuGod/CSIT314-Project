"""
TC66 - Platform Admin Updating an IDP Category (User Story #66)
Precondition: the Platform Admin is logged in and the category exists.
Each test follows one row (test step) of Matthew's test case sheet (TC66).
Run:  python -m unittest tests.test_tc66_update_idp_category -v
"""
import copy
from tests.tc_helpers import *
from entity import IDPCategory

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"


def categoryNames():
    return [c._name for c in IDPCategory._categories]

STUDY = "IDP-CAT-004"

class TC66(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedCategories = copy.deepcopy(IDPCategory._categories)
        self.savedNextID = IDPCategory._nextID
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        IDPCategory._categories = self.savedCategories
        IDPCategory._nextID = self.savedNextID
        super().tearDown()

    def test_TC66_1(self):
        # Platform Admin selects a category, clicks 'Edit', changes the name and clicks 'Save'
        html = postText(self.browser, f"/platform/idp-categories/{STUDY}/update", name="Home Office", description="Home offices and study rooms")
        self.assertIn('Category &#34;Home Office&#34; was updated.', html)
        self.assertIn("Home Office", categoryNames())
        self.assertNotIn("Study", categoryNames())

    def test_TC66_2(self):
        # Platform Admin clears the name and clicks 'Save'
        html = postText(self.browser, f"/platform/idp-categories/{STUDY}/update", name="", description="Home offices and study rooms")
        self.assertIn("Enter a category name.", html)
        self.assertIn("Study", categoryNames())

    def test_TC66_3(self):
        # Platform Admin renames it to a name that already exists and clicks 'Save'
        html = postText(self.browser, f"/platform/idp-categories/{STUDY}/update", name="Bedroom", description="Duplicate")
        self.assertIn("That category name is already taken. Choose a unique name.", html)
        self.assertIn("Study", categoryNames())


if __name__ == "__main__":
    unittest.main()

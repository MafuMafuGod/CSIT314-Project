"""
TC68 - Platform Admin Deleting an IDP Category (User Story #68)
Precondition: the Platform Admin is logged in and the category exists.
Each test follows one row (test step) of Matthew's test case sheet (TC68).
Run:  python -m unittest tests.test_tc68_delete_idp_category -v
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

class TC68(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedCategories = copy.deepcopy(IDPCategory._categories)
        self.savedNextID = IDPCategory._nextID
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        IDPCategory._categories = self.savedCategories
        IDPCategory._nextID = self.savedNextID
        super().tearDown()

    def test_TC68_1(self):
        # Platform Admin opens a category with no projects, clicks 'Delete' and confirms
        html = postText(self.browser, f"/platform/idp-categories/{STUDY}/delete")
        self.assertIn('Category &#34;Study&#34; was deleted.', html)
        self.assertNotIn("Study", categoryNames())

    def test_TC68_2(self):
        # Platform Admin clicks 'Delete', then 'Cancel' in the confirmation pop-up
        html = getText(self.browser, f"/platform/idp-categories/{STUDY}")
        self.assertIn('id="delete-modal"', html)
        self.assertIn('href="#">Cancel</a>', html)          # Cancel only closes the pop-up
        self.assertIn("Study", categoryNames())

    def test_TC68_3(self):
        # Platform Admin tries to delete a category that still has projects
        html = postText(self.browser, f"/platform/idp-categories/{KITCHEN}/delete")
        self.assertIn("This category still has 1 linked project(s). Reassign them before deleting it.", html)
        self.assertIn("Kitchen", categoryNames())


if __name__ == "__main__":
    unittest.main()

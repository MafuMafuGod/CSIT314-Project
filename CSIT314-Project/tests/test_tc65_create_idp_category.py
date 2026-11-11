"""
TC65 - Platform Admin Creating an IDP Category (User Story #65)
Precondition: the Platform Admin is logged in.
Each test follows one row (test step) of Matthew's test case sheet (TC65).
Run:  python -m unittest tests.test_tc65_create_idp_category -v
"""
import copy
from tests.tc_helpers import *
from entity import IDPCategory

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"


def categoryNames():
    return [c._name for c in IDPCategory._categories]


class TC65(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedCategories = copy.deepcopy(IDPCategory._categories)
        self.savedNextID = IDPCategory._nextID
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        IDPCategory._categories = self.savedCategories
        IDPCategory._nextID = self.savedNextID
        super().tearDown()

    def test_TC65_1(self):
        # Platform Admin enters a name and description, clicks 'Save'
        html = postText(self.browser, "/platform/idp-categories/create", name="Bathroom", description="Bathrooms and powder rooms")
        self.assertIn('Category &#34;Bathroom&#34; was created.', html)
        self.assertIn("Bathroom", categoryNames())

    def test_TC65_2(self):
        # Platform Admin leaves the name empty and clicks 'Save'
        before = len(IDPCategory._categories)
        html = postText(self.browser, "/platform/idp-categories/create", name="", description="Bathrooms and powder rooms")
        self.assertIn("Enter a category name.", html)
        self.assertEqual(before, len(IDPCategory._categories))

    def test_TC65_3(self):
        # Platform Admin enters a name that already exists and clicks 'Save'
        before = len(IDPCategory._categories)
        html = postText(self.browser, "/platform/idp-categories/create", name="Kitchen", description="Duplicate")
        self.assertIn("That category name is already taken. Choose a unique name.", html)
        self.assertEqual(before, len(IDPCategory._categories))


if __name__ == "__main__":
    unittest.main()

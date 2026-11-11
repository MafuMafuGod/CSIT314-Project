"""
TC69 - Platform Admin Searching IDP Categories (User Story #69)
Precondition: the Platform Admin is logged in and categories exist.
Each test follows one row (test step) of Matthew's test case sheet (TC69).
Run:  python -m unittest tests.test_tc69_search_idp_category -v
"""
import copy
from tests.tc_helpers import *
from entity import IDPCategory

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"


def categoryNames():
    return [c._name for c in IDPCategory._categories]


class TC69(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedCategories = copy.deepcopy(IDPCategory._categories)
        self.savedNextID = IDPCategory._nextID
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        IDPCategory._categories = self.savedCategories
        IDPCategory._nextID = self.savedNextID
        super().tearDown()

    def test_TC69_1(self):
        # Platform Admin enters a keyword and clicks Search
        html = getText(self.browser, "/platform/idp-categories/search?keyword=kit")
        self.assertIn("Kitchen", html)
        for other in ("Living Room", "Bedroom", "Whole House"):
            self.assertNotIn(f"<strong>{other}</strong>", html)
        self.assertNotIn("No categories found", html)

    def test_TC69_2(self):
        # Platform Admin leaves the search field empty and clicks Search
        html = getText(self.browser, "/platform/idp-categories/search?keyword=")
        for name in categoryNames():
            self.assertIn(name, html)

    def test_TC69_3(self):
        # Platform Admin enters a keyword that does not match and clicks Search
        html = getText(self.browser, "/platform/idp-categories/search?keyword=qwerty")
        self.assertIn("No categories found", html)


if __name__ == "__main__":
    unittest.main()

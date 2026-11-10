"""
TC32 - Customer Searching IDPs (User Story #32)
Precondition: Customer is logged in.
Run:  python -m unittest tests.test_tc32_search_idp -v
"""
from tests.tc_helpers import *


class TC32(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login()       # precondition: Customer logged in

    def test_TC32_1_open_search_page(self):
        html = getText(self.browser, "/search")
        self.assertIn('name="keyword"', html)
        for category in ["Bedroom", "Kitchen", "Living Room", "Whole House"]:
            self.assertIn(category, html)
        self.assertIn("Search", html)

    def test_TC32_2_empty_keyword_and_category(self):
        html = getText(self.browser, "/search?keyword=&category=")
        self.assertIn("Please enter a keyword or select a category.", html)

    def test_TC32_3_keyword_only(self):
        html = getText(self.browser, "/search?keyword=kitchen&category=")
        self.assertIn("1 project found", html)
        self.assertIn("Punggol Waterway Condo Kitchen", html)
        self.assertIn("View Details", html)

    def test_TC32_4_category_only(self):
        html = getText(self.browser, "/search?keyword=&category=Living Room")
        self.assertIn("Sengkang BTO Minimalist Living Room", html)
        self.assertIn("Tampines HDB Scandinavian Makeover", html)

    def test_TC32_5_keyword_and_category(self):
        html = getText(self.browser, "/search?keyword=minimalist&category=Living Room")
        self.assertIn("Sengkang BTO Minimalist Living Room", html)
        self.assertNotIn("Tampines HDB Scandinavian Makeover", html)

    def test_TC32_6_category_does_not_match(self):
        html = getText(self.browser, "/search?keyword=kitchen&category=Bedroom")
        self.assertIn("No matching IDPs were found. Try a different keyword or category.", html)

    def test_TC32_7_keyword_matches_nothing(self):
        html = getText(self.browser, "/search?keyword=castle&category=")
        self.assertIn("No matching IDPs were found. Try a different keyword or category.", html)

    def test_TC32_8_keyword_in_capital_letters(self):
        html = getText(self.browser, "/search?keyword=JAPANDI&category=")
        self.assertIn("Clementi Resale Japandi Bedroom", html)

    def test_TC32_9_keyword_too_long(self):
        html = getText(self.browser, "/search?keyword=" + "a" * 101 + "&category=")
        self.assertIn("Keyword must be 100 characters or fewer.", html)


if __name__ == "__main__":
    unittest.main()

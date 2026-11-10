"""
TC33 - Customer Viewing IDP Details (User Story #33)
Precondition: Customer is logged in.
Run:  python -m unittest tests.test_tc33_view_idp -v
"""
from tests.tc_helpers import *


class TC33(BaseTest):

    def setUp(self):
        super().setUp()
        self.browser = login()       # precondition: Customer logged in

    def test_TC33_1_view_details(self):
        html = getText(self.browser, "/idp/2")
        self.assertIn("Punggol Waterway Condo Kitchen", html)    # title
        self.assertIn("Kitchen", html)                           # category
        self.assertIn("Open kitchen with a quartz island", html) # description
        self.assertIn("Save to Favourite List", html)
        self.assertIn("Back", html)

    def test_TC33_2_back_goes_to_search_results(self):
        # the Customer came from the search results page
        page = self.browser.get("/idp/2", headers={"Referer": "http://localhost/search?keyword=kitchen&category="})
        html = page.get_data(as_text=True)
        self.assertIn('href="http://localhost/search?keyword=kitchen&amp;category="', html)

    def test_TC33_2_back_goes_to_search_when_no_previous_page(self):
        # the Customer opened the IDP address directly (no previous page)
        html = getText(self.browser, "/idp/2")
        self.assertIn('href="/search"', html)

    def test_TC33_3_view_count_goes_up_by_1(self):
        before = getIDP(2)._viewCount
        getText(self.browser, "/idp/2")
        self.assertEqual(before + 1, getIDP(2)._viewCount)

    def test_TC33_4_idp_does_not_exist(self):
        html = getText(self.browser, "/idp/999")
        self.assertIn("Sorry, this IDP could not be found. It may have been removed.", html)
        self.assertIn("Back to results", html)

    def test_TC33_4_missing_idp_is_not_counted(self):
        before = [i._viewCount for i in InteriorDesignProject._idps]
        getText(self.browser, "/idp/999")
        after = [i._viewCount for i in InteriorDesignProject._idps]
        self.assertEqual(before, after)

    def test_TC33_5_address_has_letters(self):
        response = self.browser.get("/idp/abc")
        self.assertEqual(404, response.status_code)


if __name__ == "__main__":
    unittest.main()

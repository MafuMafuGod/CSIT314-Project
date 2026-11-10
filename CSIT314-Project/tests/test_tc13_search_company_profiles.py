"""TC13: ID searches company profiles.

Place this file in the project's tests/ directory and run with:
    python -m pytest tests/test_tc13_search_company_profiles.py -v
"""
from tests.helpers import loggedIn

import app as app_module
from entity import CompanyProfile


DESIGNER_EMAIL = "designer@4reno.com"
DESIGNER_PASSWORD = "design123"


class TestTC13SearchCompanyProfiles:
    def setup_method(self):
        self._saved_profiles = list(CompanyProfile._profiles)
        CompanyProfile._profiles = [
            CompanyProfile(
                "form@4reno.com",
                "Form & Field Interiors",
                "Thought spaces for everyday living",
                "hello@formandfield.sg",
                "+65 6123 4567",
                "Singapore",
                "https://www.formandfield.sg",
            ),
            CompanyProfile(
                "other@4reno.com",
                "Other Design Studio",
                "Residential interior design",
                "hello@other.sg",
                "+65 6000 0000",
                "Singapore",
                "https://www.other.sg",
            ),
        ]
        app_module.app.config["TESTING"] = True
        self.client = loggedIn(app_module, DESIGNER_EMAIL, DESIGNER_PASSWORD)

    def teardown_method(self):
        CompanyProfile._profiles = self._saved_profiles

    def test_tc13_1_search_page_has_company_keyword_input(self):
        response = self.client.get("/designer/company-profiles/search")
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert 'name="keyword"' in html
        assert "Search Company Profiles" in html

    def test_tc13_2_keyword_returns_matching_company_and_website(self):
        response = self.client.get(
            "/designer/company-profiles/search?keyword=Form%20%26%20Field"
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "Form &amp; Field Interiors" in html or "Form & Field Interiors" in html
        assert "Thought spaces for everyday living" in html
        assert "https://www.formandfield.sg" in html
        assert "Other Design Studio" not in html

    def test_tc13_3_unmatched_keyword_shows_no_match_message(self):
        response = self.client.get(
            "/designer/company-profiles/search?keyword=no-such-company-987"
        )
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert "No matching company profiles were found." in html
        assert "Form &amp; Field Interiors" not in html
        assert "Other Design Studio" not in html


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))

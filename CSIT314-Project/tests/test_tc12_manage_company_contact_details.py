"""TC12: ID manages company contact details.

Place this file in the project's tests/ directory and run with:
    python -m pytest tests/test_tc12_manage_company_contact_details.py -v
"""
from tests.helpers import loggedIn, post

import app as app_module
from entity import CompanyProfile


DESIGNER_EMAIL = "designer@4reno.com"
DESIGNER_PASSWORD = "design123"
ORIGINAL = {
    "businessEmail": "hello@tristeninteriors.sg",
    "businessPhone": "61234567",
    "businessAddress": "1 Sengkang Square, Singapore 545078",
    "website": "https://www.tristeninteriors.sg",
    "instagram": "",
    "facebook": "",
    "linkedin": "",
}
UPDATED = {
    **ORIGINAL,
    "businessEmail": "contact@tristeninteriors.sg",
    "businessPhone": "+65 6123 4567",
    "businessAddress": "2 Sengkang Square, Singapore 545078",
}


class TestTC12ManageCompanyContactDetails:
    def setup_method(self):
        self._saved_profiles = list(CompanyProfile._profiles)
        CompanyProfile._profiles = [
            CompanyProfile(
                DESIGNER_EMAIL,
                "Tristen Interiors",
                "HDB and condo renovations with a focus on storage.",
                ORIGINAL["businessEmail"],
                ORIGINAL["businessPhone"],
                ORIGINAL["businessAddress"],
                ORIGINAL["website"],
            )
        ]
        app_module.app.config["TESTING"] = True
        self.client = loggedIn(app_module, DESIGNER_EMAIL, DESIGNER_PASSWORD)

    def teardown_method(self):
        CompanyProfile._profiles = self._saved_profiles

    def test_tc12_1_view_saved_contact_details(self):
        response = self.client.get("/designer/contact-info")
        html = response.get_data(as_text=True)

        assert response.status_code == 200
        assert ORIGINAL["businessEmail"] in html
        assert ORIGINAL["businessPhone"] in html
        assert ORIGINAL["businessAddress"] in html

    def test_tc12_2_save_and_reopen_updated_contact_details(self):
        html = post(self.client, "/designer/contact-info/save", **UPDATED)
        assert "Contact information updated successfully." in html

        reopened = self.client.get("/designer/contact-info").get_data(as_text=True)
        assert UPDATED["businessEmail"] in reopened
        assert UPDATED["businessPhone"] in reopened
        assert UPDATED["businessAddress"] in reopened

    def test_tc12_3_invalid_contact_is_rejected_and_saved_values_remain(self):
        invalid = {**UPDATED, "businessPhone": "not-a-phone"}
        html = post(self.client, "/designer/contact-info/save", **invalid)

        assert "Please correct the missing or invalid fields." in html or "valid phone number" in html
        saved = CompanyProfile.getProfile(DESIGNER_EMAIL)
        assert saved["businessPhone"] == ORIGINAL["businessPhone"]
        assert saved["businessEmail"] == ORIGINAL["businessEmail"]


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))

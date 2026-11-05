"""
Unit tests for #12 Manage company contact information and #13 Search company profiles.
Run from the project folder:   python -m pytest tests/test_company_contact.py -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import CompanyProfile                                           # noqa: E402
from control import ManageContactInfoController, SearchCompanyProfilesController   # noqa: E402
from boundary.manage_contact_info_page import validateContactInfo           # noqa: E402
from boundary.search_company_profiles_page import validateKeyword           # noqa: E402
from tests.helpers import loggedIn, post                                    # noqa: E402

ID = "designer@4reno.com"
CONTACT = {"businessEmail": "hi@dl.sg", "businessPhone": "+65 6000 1111", "businessAddress": "1 Raffles Place",
           "website": "https://dl.sg", "instagram": "@dl", "facebook": "", "linkedin": "DL Interiors"}


@pytest.fixture(autouse=True)
def fresh_profiles():
    saved = list(CompanyProfile._profiles)
    CompanyProfile._profiles = [
        CompanyProfile(ID, "Daniel Lim Interiors", "Warm, practical homes.", "daniel@dl.sg",
                       "+65 6000 0000", "2 Raffles Place"),
        CompanyProfile("nook@4reno.com", "Nook Studio", "Compact HDB makeovers", "hi@nook.sg",
                       "+65 6789 0123", "Ubi", instagram="@nookstudio"),
    ]
    yield
    CompanyProfile._profiles = saved


@pytest.fixture
def designer():
    app_module.app.config["TESTING"] = True
    return loggedIn(app_module, ID, "design123")


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_update_contact_keeps_name_and_description(self):              # #12
        assert CompanyProfile.updateContactInfo(ID, *CONTACT.values()) is True
        profile = CompanyProfile.getProfile(ID)
        assert profile["linkedin"] == "DL Interiors" and profile["companyName"] == "Daniel Lim Interiors"

    def test_update_contact_without_profile(self):
        assert CompanyProfile.updateContactInfo("nobody@4reno.com", *CONTACT.values()) is False

    def test_search_name_and_socials_sorted(self):                         # #13
        assert [p["companyName"] for p in CompanyProfile.searchProfiles("nook")] == ["Nook Studio"]
        assert [p["companyName"] for p in CompanyProfile.searchProfiles("@NOOKSTUDIO")] == ["Nook Studio"]
        assert [p["companyName"] for p in CompanyProfile.searchProfiles("raffles")] == ["Daniel Lim Interiors"]
        assert [p["companyName"] for p in CompanyProfile.searchProfiles("+65")] == ["Daniel Lim Interiors", "Nook Studio"]
        assert CompanyProfile.searchProfiles("castle") == []


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_manage_contact_controller(self):
        assert ManageContactInfoController().updateContactInfo(ID, CONTACT) is True
        assert ManageContactInfoController().getCompanyProfile(ID)["instagram"] == "@dl"

    def test_search_controller(self):
        assert SearchCompanyProfilesController().searchCompanyProfiles("daniel")[0]["companyName"] == \
            "Daniel Lim Interiors"


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_valid(self):
        assert validateContactInfo(CONTACT) == {}

    def test_same_rules_as_update_company_information(self):              # shared with #11
        errors = validateContactInfo({**CONTACT, "businessEmail": "nope", "businessPhone": "12",
                                      "website": "dl.sg", "businessAddress": ""})
        assert set(errors) == {"businessEmail", "businessPhone", "website", "businessAddress"}

    def test_social_length(self):
        assert "instagram" in validateContactInfo({**CONTACT, "instagram": "x" * 101})

    def test_keyword(self):
        assert validateKeyword("") != "" and validateKeyword("x" * 101) != "" and validateKeyword("nook") == ""


# ---------------------------------------------------------------- Boundary pages
class TestPages:
    def test_contact_form_shows_current_details(self, designer):           # #12 steps 1-2
        assert 'value="daniel@dl.sg"' in designer.get("/designer/contact-info").get_data(as_text=True)

    def test_save_contact(self, designer):                                 # #12 step 3
        html = post(designer, "/designer/contact-info/save", **CONTACT)
        assert "Contact information updated successfully." in html
        assert CompanyProfile.getProfile(ID)["businessEmail"] == "hi@dl.sg"

    def test_invalid_contact_shows_field_errors(self, designer):           # #12 alt
        html = post(designer, "/designer/contact-info/save", **{**CONTACT, "businessPhone": "abc"})
        assert "valid phone number" in html
        assert CompanyProfile.getProfile(ID)["businessPhone"] == "+65 6000 0000"

    def test_no_profile_goes_to_company_profile(self):                     # precondition
        CompanyProfile._profiles = []
        designer = loggedIn(app_module, ID, "design123")
        html = designer.get("/designer/contact-info", follow_redirects=True).get_data(as_text=True)
        assert "Create your company profile" in html and "No company profile yet" in html

    def test_view_page_shows_socials_and_button(self, designer):           # #10 + #12
        CompanyProfile.updateContactInfo(ID, *CONTACT.values())
        html = designer.get("/designer/company").get_data(as_text=True)
        assert "Manage Contact Details" in html and "DL Interiors" in html

    def test_search_page(self, designer):                                  # #13
        assert 'name="keyword"' in designer.get("/designer/company-profiles/search").get_data(as_text=True)
        html = designer.get("/designer/company-profiles/search?keyword=nook").get_data(as_text=True)
        assert "1 matching profile" in html and "Nook Studio" in html

    def test_search_empty_and_no_match(self, designer):
        assert "Enter a company name" in designer.get("/designer/company-profiles/search?keyword=").get_data(as_text=True)
        assert "No matching company profiles" in \
            designer.get("/designer/company-profiles/search?keyword=castle").get_data(as_text=True)

    def test_only_designers(self):                                         # precondition (app.py guard)
        customer = loggedIn(app_module, "customer@4reno.com", "password123")
        assert customer.get("/designer/contact-info").status_code == 302
        assert customer.get("/designer/company-profiles/search").status_code == 302

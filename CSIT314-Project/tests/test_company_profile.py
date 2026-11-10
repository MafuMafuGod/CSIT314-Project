"""
Unit tests for User Story #09 (create company profile),
                          #10 (view company profile),
                          #11 (update company information).

Written BEFORE the company profile code (test-driven development).
Updated to Dominic's fields and rules: everything required except website,
website must start with http:// or https://.
Run from the project folder:   py -m pytest tests/test_company_profile.py -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                    # noqa: E402
from entity import CompanyProfile                           # noqa: E402
from control import (CreateCompanyProfileController,        # noqa: E402
                     ViewCompanyProfileController,
                     UpdateCompanyProfileController)

HAS_PROFILE = "designer@4reno.com"
NO_PROFILE = "newdesigner@4reno.com"

GOOD = {"companyName": "Lim & Co Interiors", "description": "Modern HDB and condo makeovers.",
        "businessEmail": "hello@limco.sg", "businessPhone": "+65 6123 4567",
        "businessAddress": "10 Anson Road, Singapore 079903", "website": "https://limco.sg"}


@pytest.fixture(autouse=True)
def fresh_profiles():
    saved = list(CompanyProfile._profiles)
    CompanyProfile._profiles = [
        CompanyProfile(HAS_PROFILE, "Daniel Lim Interiors", "Warm, practical homes.",
                       "daniel@dlinteriors.sg", "+65 6000 0000", "1 Raffles Place"),
    ]
    yield
    CompanyProfile._profiles = saved


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


def login_as(client, u, profile="designer"):
    with client.session_transaction() as s:
        s["u"] = u
        s["profile"] = profile


def post(client, path, **fields):
    return client.post(path, data=fields, follow_redirects=True)


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_profileExists(self):
        assert CompanyProfile.profileExists(HAS_PROFILE) is True
        assert CompanyProfile.profileExists(NO_PROFILE) is False

    def test_createProfile_then_getProfile(self):                       # #09 step 3
        assert CompanyProfile.createProfile(NO_PROFILE, **GOOD) is True
        profile = CompanyProfile.getProfile(NO_PROFILE)
        assert profile["companyName"] == "Lim & Co Interiors"
        assert profile["website"] == "https://limco.sg"

    def test_getProfile_missing_returns_empty(self):                    # #10 alt 2a
        assert CompanyProfile.getProfile(NO_PROFILE) == {}

    def test_updateProfile_changes_fields(self):                        # #11 step 3
        assert CompanyProfile.updateProfile(HAS_PROFILE, **GOOD) is True
        assert CompanyProfile.getProfile(HAS_PROFILE)["businessAddress"] == GOOD["businessAddress"]

    def test_updateProfile_missing_returns_false(self):
        assert CompanyProfile.updateProfile(NO_PROFILE, **GOOD) is False


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_create_controller(self):
        c = CreateCompanyProfileController()
        assert c.checkProfileExists(NO_PROFILE) is False
        assert c.createCompanyProfile(NO_PROFILE, GOOD) is True

    def test_view_controller(self):
        assert ViewCompanyProfileController().getCompanyProfile(HAS_PROFILE)["companyName"] == "Daniel Lim Interiors"

    def test_update_controller(self):
        c = UpdateCompanyProfileController()
        assert c.getCompanyProfile(HAS_PROFILE)["companyName"] == "Daniel Lim Interiors"
        assert c.updateCompanyProfile(HAS_PROFILE, GOOD) is True


# ---------------------------------------------------------------- Boundary
class TestViewPage:                                                     # #10
    def test_view_shows_details_and_update_button(self, client):
        login_as(client, HAS_PROFILE)
        html = client.get("/designer/company").get_data(as_text=True)
        assert "Daniel Lim Interiors" in html and "Update Company Information" in html

    def test_view_without_profile_shows_error_and_create_button(self, client):   # 2a
        login_as(client, NO_PROFILE)
        html = client.get("/designer/company").get_data(as_text=True)
        assert "has not been created" in html and "Create Company Profile" in html


class TestCreatePage:                                                   # #09
    def test_create_valid_saves_and_shows_profile(self, client):
        login_as(client, NO_PROFILE)
        html = post(client, "/designer/company/create", **GOOD).get_data(as_text=True)
        assert "created successfully" in html and "Lim &amp; Co Interiors" in html
        assert CompanyProfile.profileExists(NO_PROFILE)

    def test_create_website_is_optional(self, client):
        login_as(client, NO_PROFILE)
        post(client, "/designer/company/create", **{**GOOD, "website": ""})
        assert CompanyProfile.profileExists(NO_PROFILE)

    @pytest.mark.parametrize("field,message", [
        ("companyName", "Please enter your company name"),
        ("description", "Please enter a company description"),
        ("businessEmail", "Please enter a business email"),
        ("businessPhone", "Please enter a business phone number"),
        ("businessAddress", "Please enter a business address"),
    ])
    def test_create_missing_required_field_shows_error(self, client, field, message):   # 2a
        login_as(client, NO_PROFILE)
        html = post(client, "/designer/company/create", **{**GOOD, field: ""}).get_data(as_text=True)
        assert message in html
        assert not CompanyProfile.profileExists(NO_PROFILE)

    def test_create_invalid_email_shows_error(self, client):            # 2a
        login_as(client, NO_PROFILE)
        html = post(client, "/designer/company/create", **{**GOOD, "businessEmail": "nope"}).get_data(as_text=True)
        assert "valid email" in html

    def test_create_invalid_website_shows_error(self, client):          # 2a
        login_as(client, NO_PROFILE)
        html = post(client, "/designer/company/create", **{**GOOD, "website": "limco.sg"}).get_data(as_text=True)
        assert "must start with http" in html
        assert not CompanyProfile.profileExists(NO_PROFILE)

    def test_create_when_profile_exists_goes_to_view(self, client):
        login_as(client, HAS_PROFILE)
        html = client.get("/designer/company/create", follow_redirects=True).get_data(as_text=True)
        assert "already have a company profile" in html

    def test_create_overlong_field_shows_error(self, client):            # 2a
        login_as(client, NO_PROFILE)
        html = post(client, "/designer/company/create", **{**GOOD, "companyName": "x" * 101}).get_data(as_text=True)
        assert "100 characters or fewer" in html
        assert not CompanyProfile.profileExists(NO_PROFILE)

    def test_create_twice_by_posting_is_blocked(self, client):          # one profile per ID
        login_as(client, HAS_PROFILE)
        html = post(client, "/designer/company/create", **GOOD).get_data(as_text=True)
        assert "already have a company profile" in html
        assert CompanyProfile.getProfile(HAS_PROFILE)["companyName"] == "Daniel Lim Interiors"


class TestUpdatePage:                                                   # #11
    def test_update_form_is_prefilled(self, client):                    # step 2
        login_as(client, HAS_PROFILE)
        html = client.get("/designer/company/update").get_data(as_text=True)
        assert 'value="Daniel Lim Interiors"' in html

    def test_update_valid_saves(self, client):                          # step 3
        login_as(client, HAS_PROFILE)
        html = post(client, "/designer/company/update", **GOOD).get_data(as_text=True)
        assert "updated successfully" in html
        assert CompanyProfile.getProfile(HAS_PROFILE)["companyName"] == "Lim & Co Interiors"

    def test_update_invalid_keeps_old_data(self, client):               # 3a
        login_as(client, HAS_PROFILE)
        html = post(client, "/designer/company/update", **{**GOOD, "description": ""}).get_data(as_text=True)
        assert "Please enter a company description" in html
        assert CompanyProfile.getProfile(HAS_PROFILE)["companyName"] == "Daniel Lim Interiors"

    def test_update_save_failure_shows_message(self, client, monkeypatch):   # profile removed meanwhile
        login_as(client, HAS_PROFILE)
        monkeypatch.setattr(CompanyProfile, "updateProfile", classmethod(lambda cls, *a, **k: False))
        html = post(client, "/designer/company/update", **GOOD).get_data(as_text=True)
        assert "Unable to save company profile" in html

    def test_update_without_profile_goes_to_view(self, client):         # precondition
        login_as(client, NO_PROFILE)
        html = client.get("/designer/company/update", follow_redirects=True).get_data(as_text=True)
        assert "has not been created" in html


class TestAccess:                                                       # preconditions
    def test_customer_is_blocked(self, client):
        login_as(client, "customer@4reno.com", "customer")
        assert client.get("/designer/company").status_code == 302

    def test_not_logged_in_goes_to_login(self, client):
        r = client.get("/designer/company")
        assert r.status_code == 302 and "/login" in r.headers["Location"]

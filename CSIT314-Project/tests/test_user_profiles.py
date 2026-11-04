"""
Unit tests for #47 Create, #48 View, #49 Update, #50 Suspend and #51 Search User Profile.
Run from the project folder:   python -m pytest tests/test_user_profiles.py -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import UserAccount, UserProfile                                 # noqa: E402
from control import (CreateUserProfileController, ViewUserProfileController,  # noqa: E402
                     SearchUserProfileController, UserLoginController)
from boundary.profiles import validateProfileDetails                        # noqa: E402
from tests.helpers import snapshot, restore, loggedIn, post        # noqa: E402

GROUPS = UserProfile.getPermissionGroups()


@pytest.fixture(autouse=True)
def fresh_data():
    saved = snapshot()
    yield
    restore(saved)


@pytest.fixture
def admin():
    app_module.app.config["TESTING"] = True
    return loggedIn(app_module, "admin@4reno.com", "admin123")


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_name_unique_case_insensitive(self):                          # #47 step 8
        assert UserProfile.profileNameExists("interior designer") is True

    def test_create_makes_unique_key(self):                                # #47 step 9
        UserProfile.createProfile("Senior Admin", "", ["View audit log"])
        assert UserProfile.selectProfile("Senior Admin")["key"] == "senior-admin"

    def test_search(self):                                                 # #51 step 4
        assert [p["name"] for p in UserProfile.searchProfiles("DESIGN", "")] == ["Interior Designer"]
        assert UserProfile.searchProfiles("", "suspended") == []           # 4a

    def test_update_missing_profile_fails(self):                           # #49 8a
        assert UserProfile.updateProfile("Nope", "X", "", ["View audit log"]) is False

    def test_suspend_only_once(self):                                      # #50 step 3
        assert UserProfile.suspendProfile("Customer", "") is True
        assert UserProfile.suspendProfile("Customer", "") is False

    def test_suspended_profile_blocks_login(self):                         # #50 step 4
        UserProfile.suspendProfile("Customer", "")
        assert UserLoginController().userAccountLogin("customer@4reno.com", "password123") is False

    def test_suspended_profile_not_assignable(self):
        UserProfile.suspendProfile("Customer", "")
        assert "customer" not in UserProfile.getActiveProfileOptions()


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_list_has_user_counts(self):                                   # #48 step 2
        counts = {p["name"]: p["userCount"] for p in ViewUserProfileController().getUserProfileList()}
        assert counts["Interior Designer"] == 1

    def test_search_has_user_counts(self):                                 # #51
        assert SearchUserProfileController().searchUserProfiles("admin", "")[0]["userCount"] == 1

    def test_start_from_permissions(self):                                 # #47
        assert CreateUserProfileController().getStartingPermissions("User Admin") == GROUPS["Administration"]
        assert CreateUserProfileController().getStartingPermissions("") == []


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_valid(self):
        assert validateProfileDetails("Senior Admin", "", ["View audit log"], GROUPS) == {}

    def test_missing_name_and_permissions(self):                           # #47 7a / #49 step 4
        errors = validateProfileDetails("", "", [], GROUPS)
        assert set(errors) == {"name", "permissions"}

    def test_bad_name_characters(self):
        assert "name" in validateProfileDetails("a/b", "", ["View audit log"], GROUPS)

    def test_unknown_permission(self):
        assert "permissions" in validateProfileDetails("X", "", ["Fly"], GROUPS)

    def test_overlong_description(self):
        assert "description" in validateProfileDetails("X", "d" * 201, ["View audit log"], GROUPS)


# ---------------------------------------------------------------- Boundary pages
class TestPages:
    def test_list(self, admin):                                            # #48 steps 1-2
        html = admin.get("/admin/profiles").get_data(as_text=True)
        assert "Showing 4 of 4 profiles" in html and "Platform Management" in html

    def test_view(self, admin):                                            # #48 steps 3-5
        html = admin.get("/admin/profiles/view/Interior%20Designer").get_data(as_text=True)
        assert html.count("&#10003; Allowed") == 3 and "designer@4reno.com" in html

    def test_view_missing_is_404(self, admin):
        assert admin.get("/admin/profiles/view/Nope").status_code == 404

    def test_search_and_no_match(self, admin):                             # #51
        assert "Interior Designer" in admin.get("/admin/profiles?q=design").get_data(as_text=True)
        assert "No user profiles found" in admin.get("/admin/profiles?q=zzz").get_data(as_text=True)

    def test_create_and_use_in_account_form(self, admin):                  # #47 -> #42
        html = post(admin, "/admin/profiles/create", name="Senior Admin", description="Audit",
                    permissions=["View audit log"])
        assert "Profile summary" in html and "Senior Admin" in html
        assert 'value="senior-admin"' in admin.get("/admin/users/create").get_data(as_text=True)

    def test_create_duplicate_name(self, admin):                           # #47 step 8
        html = post(admin, "/admin/profiles/create", name="customer", permissions=["Search IDPs"])
        assert "already exists" in html

    def test_create_start_from(self, admin):
        html = admin.get("/admin/profiles/create?start=User%20Admin").get_data(as_text=True)
        assert 'value="View audit log" checked' in html

    def test_update_and_changes(self, admin):                              # #49 steps 4-6
        html = post(admin, "/admin/profiles/edit/Customer", name="Homeowner", description="",
                    permissions=["Search IDPs"])
        assert "Customer → Homeowner" in html and "Removed View IDP details, Manage shortlist" in html
        assert UserAccount.getProfile("customer@4reno.com") == "customer"  # key unchanged

    def test_suspend_profile_blocks_its_users(self, admin):                # #50
        customer = loggedIn(app_module, "customer@4reno.com", "password123")
        html = post(admin, "/admin/profiles/suspend/Customer", reason="Maintenance")
        assert "has been suspended" in html and "Blocked" in html
        html = customer.get("/search", follow_redirects=True).get_data(as_text=True)
        assert "Your account has been suspended" in html

    def test_cannot_suspend_own_profile(self, admin):
        assert "cannot suspend your own profile" in post(admin, "/admin/profiles/suspend/User%20Admin")

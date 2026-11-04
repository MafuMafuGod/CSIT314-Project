"""
Unit tests for #42 Create, #43 View, #44 Update, #45 Suspend and #46 Search User Account.
Run from the project folder:   python -m pytest tests/test_user_accounts.py -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import UserAccount                                              # noqa: E402
from control import (UpdateUserAccountController, SuspendUserAccountController,   # noqa: E402
                     SearchUserAccountController, UserLoginController)
from boundary.view_user_account_page import validateSearchCriteria          # noqa: E402
from tests.helpers import snapshot, restore, loggedIn, post        # noqa: E402


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
    def test_search_by_name_or_email_case_insensitive(self):              # #46 step 5
        assert [a["u"] for a in UserAccount.searchAccounts("DANIEL", "", "")] == ["designer@4reno.com"]
        assert [a["u"] for a in UserAccount.searchAccounts("customer@", "", "")] == ["customer@4reno.com"]

    def test_search_by_profile_and_status(self):
        assert len(UserAccount.searchAccounts("", "active", "")) == 4
        assert UserAccount.searchAccounts("", "suspended", "") == []      # 7a
        assert [a["u"] for a in UserAccount.searchAccounts("", "", "admin")] == ["admin@4reno.com"]

    def test_update_account(self):                                         # #44 step 4
        assert UserAccount.updateAccount("customer@4reno.com", "Hannah T", "hannah@4reno.com",
                                         "designer", ["Manage own IDPs"])
        a = UserAccount.selectUserAccount("hannah@4reno.com")
        assert (a["name"], a["profile"], a["permissions"]) == ("Hannah T", "designer", ["Manage own IDPs"])

    def test_suspend_only_once(self):                                      # #45 step 5
        assert UserAccount.suspendAccount("customer@4reno.com", "reason") is True
        assert UserAccount.suspendAccount("customer@4reno.com", "reason") is False
        assert UserAccount.suspendAccount("nobody@4reno.com", "") is False

    def test_suspended_account_cannot_log_in(self):                        # #45 step 6
        UserAccount.suspendAccount("customer@4reno.com", "")
        assert UserLoginController().userAccountLogin("customer@4reno.com", "password123") is False

    def test_login_records_last_sign_in(self):
        UserLoginController().userAccountLogin("customer@4reno.com", "password123")
        assert UserAccount.selectUserAccount("customer@4reno.com")["lastSignIn"]


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_search_controller_passes_entity_result_through(self):
        assert SearchUserAccountController().searchUserAccounts("dan", "", "") == \
            UserAccount.searchAccounts("dan", "", "")

    def test_update_controller_checks_email(self):
        assert UpdateUserAccountController().checkAccountExists("CUSTOMER@4reno.com") is True

    def test_suspend_controller(self):
        assert SuspendUserAccountController().suspendUserAccount("designer@4reno.com", "") is True


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_valid_search(self):                                           # #46 step 4
        assert validateSearchCriteria("dan", "active", "designer") == ""

    def test_unknown_status_or_profile_rejected(self):
        assert validateSearchCriteria("", "invited", "") != ""
        assert validateSearchCriteria("", "", "pilot") != ""

    def test_overlong_search_rejected(self):
        assert validateSearchCriteria("x" * 101, "", "") != ""


# ---------------------------------------------------------------- Boundary pages
class TestPages:
    def test_list_and_search(self, admin):                                 # #43 / #46
        assert admin.get("/admin/users").get_data(as_text=True).count("@4reno.com</td>") == 4
        html = admin.get("/admin/users?q=dan").get_data(as_text=True)
        assert "designer@4reno.com" in html and "customer@4reno.com</td>" not in html

    def test_search_no_match_message(self, admin):                         # #46 7a
        assert "No user accounts found" in admin.get("/admin/users?q=zzz").get_data(as_text=True)

    def test_create_saves_permissions(self, admin):                        # #42
        html = post(admin, "/admin/users/create", name="Mei", u="mei@4reno.com", p="pw",
                    profile="designer", permissions=["Manage own IDPs"])
        assert "created successfully" in html
        assert UserAccount.selectUserAccount("mei@4reno.com")["permissions"] == ["Manage own IDPs"]

    def test_create_rejects_unknown_profile(self, admin):                  # #42 6a
        html = post(admin, "/admin/users/create", name="Mei", u="mei@4reno.com", p="pw", profile="pilot")
        assert "Please select a profile." in html

    def test_edit_form_shows_current_details(self, admin):                 # #44 step 1
        html = admin.get("/admin/users/edit/customer@4reno.com").get_data(as_text=True)
        assert 'value="Hannah Tan"' in html and 'value="Search IDPs" checked' in html

    def test_edit_validation_errors(self, admin):                          # #44 5a
        html = post(admin, "/admin/users/edit/customer@4reno.com", name="", u="bad", profile="customer")
        assert "Please enter the user&#39;s name." in html and "valid email" in html

    def test_edit_duplicate_email(self, admin):                            # #44 step 3
        html = post(admin, "/admin/users/edit/customer@4reno.com", name="H", u="designer@4reno.com",
                    profile="customer")
        assert "already exists" in html

    def test_edit_saves_and_shows_changes(self, admin):                    # #44 steps 4-5
        html = post(admin, "/admin/users/edit/customer@4reno.com", name="Hannah T",
                    u="customer@4reno.com", profile="customer", permissions=["Search IDPs"])
        assert "What changed" in html and "Hannah Tan → Hannah T" in html
        assert "Removed View IDP details, Manage shortlist" in html

    def test_suspend_and_session_ends(self, admin):                        # #45
        customer = loggedIn(app_module, "customer@4reno.com", "password123")
        html = post(admin, "/admin/users/suspend/customer@4reno.com", reason="Left")
        assert "has been suspended" in html and "Left" in html
        html = customer.get("/search", follow_redirects=True).get_data(as_text=True)
        assert "Your account has been suspended" in html                   # step 5: session ended

    def test_cannot_suspend_self(self, admin):
        assert "cannot suspend your own account" in post(admin, "/admin/users/suspend/admin@4reno.com")

    def test_non_admin_is_turned_away(self):                               # #45 6b (precondition)
        customer = loggedIn(app_module, "customer@4reno.com", "password123")
        assert customer.post("/admin/users/suspend/designer@4reno.com",
                             data={"csrf_token": "t"}).status_code == 302
        assert UserAccount.selectUserAccount("designer@4reno.com")["status"] == "active"

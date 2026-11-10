"""
Unit tests for #34 Save IDP to Shortlist, #35 Search Shortlist, #36 View Shortlisted IDP
and #37 Customer Logout.
Run from the project folder:   python -m pytest tests/test_shortlist.py -v
"""
import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import InteriorDesignProject, Shortlist                         # noqa: E402
from control import (SaveIDPController, SearchShortlistController,         # noqa: E402
                     ViewShortlistedIDPController)
from boundary.search_shortlist_page import validateKeyword                  # noqa: E402
from tests.helpers import loggedIn, post                                    # noqa: E402

CUSTOMER = "customer@4reno.com"


@pytest.fixture(autouse=True)
def fresh_data():
    saved = (copy.deepcopy(Shortlist._entries), list(InteriorDesignProject._idps))
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, "d@4reno.com", "Tampines HDB Makeover", "2026-09-01", 10, 2,
                              description="Light oak floors", category="Living Room"),
        InteriorDesignProject(2, "d@4reno.com", "Punggol Condo Kitchen", "2026-10-05", 25, 7,
                              description="Quartz island", category="Kitchen"),
    ]
    Shortlist._entries = [Shortlist(CUSTOMER, 2)]
    yield
    Shortlist._entries, InteriorDesignProject._idps = saved


@pytest.fixture
def customer():
    app_module.app.config["TESTING"] = True
    return loggedIn(app_module, CUSTOMER, "password123")


def counts(idpID):
    row = [r for r in InteriorDesignProject.getShortlistCounts("d@4reno.com") if r["idpID"] == idpID][0]
    views = [r for r in InteriorDesignProject.getViewCounts("d@4reno.com") if r["idpID"] == idpID][0]
    return row["shortlistCount"], views["viewCount"]


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_isSaved(self):                                                # #34 step 3 / #36 step 4
        assert Shortlist.isSaved(CUSTOMER, 2) is True
        assert Shortlist.isSaved(CUSTOMER, 1) is False
        assert Shortlist.isSaved("someone@4reno.com", 2) is False

    def test_saved_ids_newest_first(self):                                 # #35 step 5
        Shortlist.saveIDP(CUSTOMER, 1)
        assert Shortlist.getSavedIDPIDs(CUSTOMER) == [1, 2]

    def test_getIDPCards_filters_by_keyword(self):                         # #35 step 6
        assert [c["idpID"] for c in InteriorDesignProject.getIDPCards([1, 2], "quartz")] == [2]
        assert InteriorDesignProject.getIDPCards([1, 2], "castle") == []    # 6a

    def test_getIDPCards_skips_removed_idps(self):
        assert InteriorDesignProject.getIDPCards([2, 999]) == InteriorDesignProject.getIDPCards([2])


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_save_counts_for_41(self):                                     # #34 step 4 -> #41
        assert SaveIDPController().saveIDP(CUSTOMER, 1) is True
        assert counts(1) == (3, 10)                                        # shortlist +1, views unchanged

    def test_save_missing_idp_fails(self):                                 # #34 4a
        assert SaveIDPController().saveIDP(CUSTOMER, 999) is False
        assert Shortlist.getSavedIDPIDs(CUSTOMER) == [2]

    def test_search_shortlist_only_searches_own_saved(self):               # #35
        assert [c["idpID"] for c in SearchShortlistController().searchShortlist(CUSTOMER, "oak")] == []

    def test_view_checks_shortlist(self):                                  # #36 step 4
        assert ViewShortlistedIDPController().isInShortlist(CUSTOMER, 1) is False


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_empty_keyword_rejected(self):                                 # #35 3a
        assert validateKeyword("") != ""

    def test_overlong_keyword_rejected(self):
        assert validateKeyword("x" * 101) != ""

    def test_keyword_ok(self):
        assert validateKeyword("kitchen") == ""


# ---------------------------------------------------------------- Boundary pages
class TestSavePage:                                                         # #34
    def test_save_confirms_and_lists(self, customer):
        html = post(customer, "/idp/1/save")
        assert "IDP saved to your favourite list." in html and "Tampines HDB Makeover" in html
        assert Shortlist.isSaved(CUSTOMER, 1)

    def test_save_twice_is_not_duplicated(self, customer):                 # 3a
        html = post(customer, "/idp/2/save")
        assert "already in your favourite list" in html
        assert Shortlist.getSavedIDPIDs(CUSTOMER) == [2] and counts(2)[0] == 7

    def test_save_missing_idp_shows_error(self, customer):                 # 4a
        assert "could not be saved" in post(customer, "/idp/999/save")


class TestShortlistPage:                                                    # #35
    def test_open_lists_saved(self, customer):                             # steps 1-2
        html = customer.get("/shortlist").get_data(as_text=True)
        assert "1 saved project" in html and "Punggol Condo Kitchen" in html

    def test_missing_keyword(self, customer):                              # 3a
        assert "Please enter a keyword" in customer.get("/shortlist?keyword=").get_data(as_text=True)

    def test_search_match_and_no_match(self, customer):                    # steps 5-7 / 6a
        assert "Punggol Condo Kitchen" in customer.get("/shortlist?keyword=quartz").get_data(as_text=True)
        assert "No matching saved projects" in customer.get("/shortlist?keyword=castle").get_data(as_text=True)

    def test_empty_shortlist(self, customer):                              # 5a
        Shortlist._entries = []
        assert "Your Shortlist is empty" in customer.get("/shortlist").get_data(as_text=True)
        assert "Your Shortlist is empty" in customer.get("/shortlist?keyword=x").get_data(as_text=True)


class TestViewShortlistedPage:                                              # #36
    def test_view_saved_project(self, customer):                           # steps 3-7
        html = customer.get("/shortlist/2").get_data(as_text=True)
        assert "Punggol Condo Kitchen" in html and "Back to" in html

    def test_not_in_shortlist(self, customer):                             # 4a
        html = customer.get("/shortlist/1").get_data(as_text=True)
        assert "not in your Shortlist" in html and "Tampines" not in html

    def test_saved_project_no_longer_available(self, customer):            # 5a
        InteriorDesignProject._idps = [i for i in InteriorDesignProject._idps if i._idpID != 2]
        assert "no longer available" in customer.get("/shortlist/2").get_data(as_text=True)


class TestAccess:                                                           # preconditions
    def test_not_logged_in_goes_to_login(self):
        r = app_module.app.test_client().get("/shortlist")
        assert r.status_code == 302 and "/login" in r.headers["Location"]

    def test_designer_has_no_shortlist(self):
        designer = loggedIn(app_module, "designer@4reno.com", "design123")
        assert designer.get("/shortlist").status_code == 302


class TestLogout:                                                           # #37
    def test_logout_ends_session(self, customer):                          # steps 1-4
        assert "You have been logged out" in post(customer, "/logout")
        assert customer.get("/shortlist").status_code == 302

    def test_already_logged_out_goes_to_login(self):                       # 2a
        client = app_module.app.test_client()
        r = client.post("/logout")
        assert r.status_code == 302 and "/login" in r.headers["Location"]

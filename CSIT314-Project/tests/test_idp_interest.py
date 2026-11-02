"""
Unit tests for User Story #40 (track/display IDP view count)
           and User Story #41 (track/display IDP shortlist count).

Written BEFORE idp_interest.py (test-driven development).
Run from the project folder:   python -m pytest tests/test_idp_interest.py -v
(Imports changed to entity/ and control/ after the Boundary/Control/Entity split.)
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                   # noqa: E402
from entity import InteriorDesignProject                    # noqa: E402
from control import (ViewIDPViewCountController,           # noqa: E402
                     ViewIDPShortlistCountController)

DESIGNER = "designer@4reno.com"
NEW_DESIGNER = "newdesigner@4reno.com"      # a designer with no IDPs (alt flow 2a)


@pytest.fixture(autouse=True)
def fresh_idps():
    """Every test starts from the same known data."""
    saved = list(InteriorDesignProject._idps)
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, DESIGNER, "Tampines HDB Makeover", "2026-09-01", 10, 2),
        InteriorDesignProject(2, DESIGNER, "Punggol Condo Kitchen", "2026-10-05", 25, 7),
        InteriorDesignProject(3, "other@4reno.com", "Bishan Landed Revamp", "2026-08-11", 99, 30),
    ]
    yield
    InteriorDesignProject._idps = saved


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


def login_as(client, u, profile):
    with client.session_transaction() as s:
        s["u"] = u
        s["profile"] = profile


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_getViewCounts_returns_only_this_designers_idps(self):
        rows = InteriorDesignProject.getViewCounts(DESIGNER)
        assert {r["title"] for r in rows} == {"Tampines HDB Makeover", "Punggol Condo Kitchen"}

    def test_getViewCounts_sorted_highest_first(self):
        rows = InteriorDesignProject.getViewCounts(DESIGNER)
        assert [r["viewCount"] for r in rows] == [25, 10]

    def test_getViewCounts_has_name_date_and_views(self):          # #40 step 3
        row = InteriorDesignProject.getViewCounts(DESIGNER)[0]
        assert set(row) >= {"idpID", "title", "createdDate", "viewCount"}

    def test_getShortlistCounts_sorted_highest_first(self):        # #41 step 3
        rows = InteriorDesignProject.getShortlistCounts(DESIGNER)
        assert [r["shortlistCount"] for r in rows] == [7, 2]
        assert set(rows[0]) >= {"idpID", "title", "createdDate", "shortlistCount"}

    def test_designer_with_no_idps_gets_empty_list(self):          # alt flow 2a
        assert InteriorDesignProject.getViewCounts(NEW_DESIGNER) == []
        assert InteriorDesignProject.getShortlistCounts(NEW_DESIGNER) == []

    def test_incrementViewCount_tracks_a_customer_view(self):      # called by #33
        assert InteriorDesignProject.incrementViewCount(1) is True
        assert InteriorDesignProject.getViewCounts(DESIGNER)[-1]["viewCount"] == 11

    def test_incrementShortlistCount_tracks_a_save(self):          # called by #34
        assert InteriorDesignProject.incrementShortlistCount(1) is True
        rows = {r["idpID"]: r for r in InteriorDesignProject.getShortlistCounts(DESIGNER)}
        assert rows[1]["shortlistCount"] == 3

    def test_increment_unknown_idp_returns_false(self):
        assert InteriorDesignProject.incrementViewCount(999) is False
        assert InteriorDesignProject.incrementShortlistCount(999) is False


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_view_count_controller_passes_entity_result_through(self):
        assert ViewIDPViewCountController().getViewCounts(DESIGNER) == \
            InteriorDesignProject.getViewCounts(DESIGNER)

    def test_shortlist_count_controller_passes_entity_result_through(self):
        assert ViewIDPShortlistCountController().getShortlistCounts(DESIGNER) == \
            InteriorDesignProject.getShortlistCounts(DESIGNER)


# ---------------------------------------------------------------- Boundary
class TestBoundary:
    def test_views_tab_shows_project_names_and_counts(self, client):        # #40
        login_as(client, DESIGNER, "designer")
        html = client.get("/designer/interest/views").get_data(as_text=True)
        assert "Punggol Condo Kitchen" in html and ">25<" in html
        assert "Bishan Landed Revamp" not in html          # someone else's IDP

    def test_shortlist_tab_shows_shortlist_counts(self, client):            # #41
        login_as(client, DESIGNER, "designer")
        html = client.get("/designer/interest/shortlists").get_data(as_text=True)
        assert "Punggol Condo Kitchen" in html and ">7<" in html

    def test_no_idp_message_and_link_to_portfolio(self, client):            # 2a
        login_as(client, NEW_DESIGNER, "designer")
        for path in ("/designer/interest/views", "/designer/interest/shortlists"):
            html = client.get(path).get_data(as_text=True)
            assert "No IDP found" in html
            assert "Create IDP" in html

    def test_customer_cannot_open_interest_page(self, client):              # precondition
        login_as(client, "customer@4reno.com", "customer")
        r = client.get("/designer/interest/views")
        assert r.status_code == 302

    def test_not_logged_in_is_sent_to_login(self, client):                  # precondition
        r = client.get("/designer/interest/views")
        assert r.status_code == 302 and "/login" in r.headers["Location"]

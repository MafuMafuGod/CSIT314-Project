"""
Unit tests for User Story #32 (Customer searches for IDPs).
Run from the project folder:   python -m pytest tests/test_search_idp.py -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                   # noqa: E402
from entity import InteriorDesignProject                    # noqa: E402
from control import SearchIDPController                     # noqa: E402
from boundary.search_idp_page import validateSearch         # noqa: E402

CATEGORIES = ["Bedroom", "Kitchen", "Living Room"]


@pytest.fixture(autouse=True)
def fresh_idps():
    """Every test starts from the same known data."""
    saved = list(InteriorDesignProject._idps)
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, "d@4reno.com", "Tampines HDB Makeover", "2026-09-01",
                              description="Scandinavian living room", category="Living Room"),
        InteriorDesignProject(2, "d@4reno.com", "Punggol Condo Kitchen", "2026-10-05",
                              description="Quartz island", category="Kitchen"),
        InteriorDesignProject(3, "d@4reno.com", "Clementi Japandi Bedroom", "2026-10-19",
                              description="Timber bed, linen", category="Bedroom"),
    ]
    yield
    InteriorDesignProject._idps = saved


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_getCategories_sorted_and_unique(self):                       # step 2
        assert InteriorDesignProject.getCategories() == CATEGORIES

    def test_keyword_matches_title_case_insensitive(self):                # step 6
        rows = InteriorDesignProject.findMatchingIDPs("punggol", "")
        assert [r["idpID"] for r in rows] == [2]

    def test_keyword_matches_description(self):
        rows = InteriorDesignProject.findMatchingIDPs("scandinavian", "")
        assert [r["idpID"] for r in rows] == [1]

    def test_category_only(self):
        rows = InteriorDesignProject.findMatchingIDPs("", "Bedroom")
        assert [r["idpID"] for r in rows] == [3]

    def test_keyword_and_category_must_both_match(self):
        assert InteriorDesignProject.findMatchingIDPs("punggol", "Bedroom") == []

    def test_no_match_returns_empty_list(self):                           # 6a
        assert InteriorDesignProject.findMatchingIDPs("castle", "") == []

    def test_result_card_has_display_fields(self):
        row = InteriorDesignProject.findMatchingIDPs("punggol", "")[0]
        assert set(row) >= {"idpID", "title", "category", "imageURL"}


# ---------------------------------------------------------------- Control
class TestController:
    def test_controller_passes_entity_results_through(self):
        assert SearchIDPController().searchIDPs("kitchen", "") == \
            InteriorDesignProject.findMatchingIDPs("kitchen", "")

    def test_controller_returns_categories(self):
        assert SearchIDPController().getCategories() == CATEGORIES


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_empty_search_is_rejected(self):                              # 5a
        assert validateSearch("", "", CATEGORIES) != ""

    def test_keyword_only_is_valid(self):
        assert validateSearch("kitchen", "", CATEGORIES) == ""

    def test_category_only_is_valid(self):
        assert validateSearch("", "Kitchen", CATEGORIES) == ""

    def test_unknown_category_is_rejected(self):
        assert validateSearch("", "Garage", CATEGORIES) != ""

    def test_overlong_keyword_is_rejected(self):
        assert validateSearch("x" * 101, "", CATEGORIES) != ""


# ---------------------------------------------------------------- Boundary pages
class TestBoundary:
    def test_open_page_shows_form_without_results(self, client):          # steps 1-2
        html = client.get("/search").get_data(as_text=True)
        assert 'name="keyword"' in html and "Kitchen" in html
        assert "found" not in html

    def test_empty_search_shows_prompt(self, client):                     # 5a
        html = client.get("/search?keyword=&category=").get_data(as_text=True)
        assert "Please enter a keyword or select a category." in html

    def test_matching_search_shows_cards(self, client):                   # step 7
        html = client.get("/search?keyword=punggol&category=").get_data(as_text=True)
        assert "1 project found" in html and "Punggol Condo Kitchen" in html
        assert "Clementi Japandi Bedroom" not in html

    def test_category_chip_search(self, client):
        html = client.get("/search?category=Bedroom").get_data(as_text=True)
        assert "Clementi Japandi Bedroom" in html

    def test_no_match_shows_message(self, client):                        # 6a
        html = client.get("/search?keyword=castle&category=").get_data(as_text=True)
        assert "No matching IDPs were found" in html

    def test_view_details_link_works(self, client):                       # step 8 -> #33
        html = client.get("/idp/2").get_data(as_text=True)
        assert "Punggol Condo Kitchen" in html

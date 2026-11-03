"""
Unit tests for User Story #33 (Customer views the details of an IDP).
Run from the project folder:   python -m pytest tests/test_view_idp.py -v
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                   # noqa: E402
from entity import InteriorDesignProject                    # noqa: E402
from control import ViewIDPController                       # noqa: E402


@pytest.fixture(autouse=True)
def fresh_idps():
    """Every test starts from the same known data."""
    saved = list(InteriorDesignProject._idps)
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, "d@4reno.com", "Tampines HDB Makeover", "2026-09-01", 10, 2,
                              description="Light oak floors", category="Living Room"),
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
    def test_findIDPByID_returns_details(self):                          # step 3
        idp = InteriorDesignProject.findIDPByID(1)
        assert idp["title"] == "Tampines HDB Makeover"
        assert set(idp) >= {"idpID", "title", "description", "category", "imageURL"}

    def test_findIDPByID_unknown_returns_empty(self):                    # 3a
        assert InteriorDesignProject.findIDPByID(999) == {}


# ---------------------------------------------------------------- Control
class TestController:
    def test_viewIDPDetails_returns_idp(self):
        assert ViewIDPController().viewIDPDetails(1)["idpID"] == 1

    def test_view_is_counted_for_40(self):                               # feeds #40
        ViewIDPController().viewIDPDetails(1)
        assert InteriorDesignProject.getViewCounts("d@4reno.com")[0]["viewCount"] == 11

    def test_unknown_idp_is_not_counted(self):
        assert ViewIDPController().viewIDPDetails(999) == {}
        assert InteriorDesignProject.getViewCounts("d@4reno.com")[0]["viewCount"] == 10


# ---------------------------------------------------------------- Boundary
class TestBoundary:
    def test_details_page_shows_idp(self, client):                       # step 4
        html = client.get("/idp/1").get_data(as_text=True)
        assert "Tampines HDB Makeover" in html and "Light oak floors" in html
        assert "Living Room" in html

    def test_back_link_returns_to_previous_list(self, client):           # step 5
        html = client.get("/idp/1", headers={"Referer": "http://localhost/search?keyword=oak"}) \
                     .get_data(as_text=True)
        assert 'href="http://localhost/search?keyword=oak"' in html

    def test_back_link_defaults_to_search(self, client):
        html = client.get("/idp/1").get_data(as_text=True)
        assert 'href="/search"' in html

    def test_unknown_idp_shows_error_and_back_link(self, client):        # 3a
        html = client.get("/idp/999").get_data(as_text=True)
        assert "could not be found" in html and 'href="/search"' in html

    def test_non_number_id_is_404(self, client):
        assert client.get("/idp/abc").status_code == 404

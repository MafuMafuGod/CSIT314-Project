"""
Unit tests for the Interior Designer's portfolio:
  current projects #52 Create, #53 View, #54 Update, #55 Delete, #56 Search
  past projects    #57 Create, #58 View, #59 Update, #60 Delete, #61 Search
Run from the project folder:   python -m pytest tests/test_portfolio.py -v
"""
import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import InteriorDesignProject                                    # noqa: E402
from control import (CreateCurrentProjectController, CreatePastProjectController,   # noqa: E402
                     ViewCurrentProjectController, ViewPastProjectController,
                     UpdateCurrentProjectController, DeletePastProjectController,
                     SearchCurrentProjectController, SearchPastProjectController)
from control.portfolio_project_controller import PortfolioProjectController  # noqa: E402
from boundary.portfolio_forms import validateForm                           # noqa: E402
from tests.helpers import loggedIn, post                                    # noqa: E402

ID = "designer@4reno.com"
OTHER = "other@4reno.com"
GOOD = {"title": "Bedok Condo Study", "description": "Home office for two",
        "designs": "Warm minimalist", "materials": "Oak, linen", "category": "Study"}
TOMORROW = (date.today() + timedelta(days=1)).isoformat()


@pytest.fixture(autouse=True)
def fresh_idps():
    saved = list(InteriorDesignProject._idps)
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, ID, "Tampines HDB Makeover", "2026-08-14", description="Light oak floors",
                              designs="Scandinavian", materials="Oak vinyl", status="Past",
                              completionDate="2026-08-10"),
        InteriorDesignProject(2, ID, "Sengkang BTO Living Room", "2026-10-08", description="Minimalist",
                              designs="Hidden storage", materials="Fluted glass"),
        InteriorDesignProject(3, OTHER, "Someone Else's Project", "2026-10-01", materials="Glass"),
    ]
    yield
    InteriorDesignProject._idps = saved


@pytest.fixture
def designer():
    app_module.app.config["TESTING"] = True
    return loggedIn(app_module, ID, "design123")


def titles(projects):
    return [p["title"] for p in projects]


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_lists_split_by_status_and_owner(self):                        # #53 step 1 / #58
        assert titles(InteriorDesignProject.getProjectsByStatus(ID, "Current")) == ["Sengkang BTO Living Room"]
        assert titles(InteriorDesignProject.getProjectsByStatus(ID, "Past")) == ["Tampines HDB Makeover"]

    def test_getProject_needs_owner_and_status(self):                      # #53 3a / #58 2a
        assert InteriorDesignProject.getProject(ID, 2, "Current")["designs"] == "Hidden storage"
        assert InteriorDesignProject.getProject(ID, 2, "Past") == {}
        assert InteriorDesignProject.getProject(ID, 3, "Current") == {}    # not this ID's

    def test_create_gets_new_id_and_status(self):                          # #52 / #57 step 6
        InteriorDesignProject.createProject(ID, "New", "D", "X", "M", "", "Past", "2026-01-01")
        project = InteriorDesignProject.getProject(ID, 4, "Past")
        assert project["status"] == "Past" and project["completionDate"] == "2026-01-01"

    def test_update_and_delete_only_own(self):                             # #54 7a / #55 4a
        assert InteriorDesignProject.updateProject(ID, 3, "Current", "x", "x", "x", "x", "") is False
        assert InteriorDesignProject.deleteProject(ID, 3, "Current") is False
        assert InteriorDesignProject.deleteProject(ID, 2, "Current") is True
        assert InteriorDesignProject.findIDPByID(2) == {}

    def test_search_covers_designs_and_materials(self):                    # #56 / #61 step 3
        assert titles(InteriorDesignProject.searchProjects(ID, "Current", "fluted")) == ["Sengkang BTO Living Room"]
        assert titles(InteriorDesignProject.searchProjects(ID, "Past", "scandi")) == ["Tampines HDB Makeover"]
        assert InteriorDesignProject.searchProjects(ID, "Current", "glass") == \
            InteriorDesignProject.searchProjects(ID, "Current", "fluted")  # not the other ID's "Glass"


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_subclasses_set_status(self):                                  # inheritance
        assert issubclass(CreateCurrentProjectController, PortfolioProjectController)
        assert (CreateCurrentProjectController.STATUS, CreatePastProjectController.STATUS) == ("Current", "Past")

    def test_create_current_saves_current(self):                           # #52 step 6
        CreateCurrentProjectController().createProject(ID, **GOOD)
        assert "Bedok Condo Study" in titles(ViewCurrentProjectController().getProjectList(ID))

    def test_create_past_saves_past(self):                                 # #57 step 6
        CreatePastProjectController().createProject(ID, **GOOD, completionDate="2026-05-01")
        assert "Bedok Condo Study" in titles(ViewPastProjectController().getProjectList(ID))

    def test_view_controllers_keep_kinds_apart(self):                      # #53 / #58
        assert ViewCurrentProjectController().getProject(ID, 1) == {}
        assert ViewPastProjectController().getProject(ID, 1)["title"] == "Tampines HDB Makeover"

    def test_update_and_delete_controllers(self):                          # #54 / #60
        assert UpdateCurrentProjectController().updateProject(ID, 2, **GOOD) is True
        assert DeletePastProjectController().deleteProject(ID, 2) is False  # 2 is current, not past

    def test_search_controllers(self):                                     # #56 / #61
        assert titles(SearchCurrentProjectController().searchProjects(ID, "minimal")) == ["Sengkang BTO Living Room"]
        assert SearchPastProjectController().searchProjects(ID, "minimal") == []


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_valid_current(self):
        assert validateForm({**GOOD, "completionDate": ""}, "current") == {}

    def test_required_fields(self):                                        # #52 5a / #54 6a
        errors = validateForm({f: "" for f in [*GOOD, "completionDate"]}, "current")
        assert set(errors) == {"title", "description", "designs", "materials"}

    def test_past_needs_real_past_date(self):                              # #57 5a / #59 6a
        assert "completionDate" in validateForm({**GOOD, "completionDate": ""}, "past")
        assert "completionDate" in validateForm({**GOOD, "completionDate": TOMORROW}, "past")
        assert "completionDate" in validateForm({**GOOD, "completionDate": "2026-02-30"}, "past")
        assert validateForm({**GOOD, "completionDate": "2026-01-15"}, "past") == {}

    def test_too_long(self):
        assert "title" in validateForm({**GOOD, "title": "x" * 101, "completionDate": ""}, "current")


# ---------------------------------------------------------------- Boundary pages
class TestPages:
    def test_portfolio_lists_current_and_past(self, designer):             # #53 / #58 step 1
        assert "Sengkang BTO Living Room" in designer.get("/designer/portfolio").get_data(as_text=True)
        html = designer.get("/designer/portfolio?kind=past").get_data(as_text=True)
        assert "Tampines HDB Makeover" in html and "Sengkang" not in html

    def test_create_current(self, designer):                               # #52
        html = post(designer, "/designer/portfolio/create/current", **GOOD)
        assert "created successfully" in html and "Bedok Condo Study" in html

    def test_create_errors(self, designer):                                # #52 5a
        html = post(designer, "/designer/portfolio/create/current", **{**GOOD, "materials": ""})
        assert "Please list the materials." in html

    def test_create_past_future_date(self, designer):                      # #57 5a
        html = post(designer, "/designer/portfolio/create/past", **GOOD, completionDate=TOMORROW)
        assert "cannot be in the future" in html

    def test_view(self, designer):                                         # #53 step 4 / #58 step 3
        html = designer.get("/designer/portfolio/past/1").get_data(as_text=True)
        assert "Scandinavian" in html and "Oak vinyl" in html and "2026-08-10" in html

    def test_view_unavailable(self, designer):                             # #53 3a / #58 2a
        for url in ("/designer/portfolio/current/1", "/designer/portfolio/current/3",
                    "/designer/portfolio/past/999"):
            assert "information is unavailable" in designer.get(url).get_data(as_text=True)

    def test_edit_prefilled_and_save(self, designer):                      # #54 steps 2-8
        assert 'value="Sengkang BTO Living Room"' in designer.get("/designer/portfolio/current/2/edit").get_data(as_text=True)
        html = post(designer, "/designer/portfolio/current/2/edit", **GOOD)
        assert "updated successfully" in html and "Bedok Condo Study" in html

    def test_edit_errors_and_save_failed(self, designer):                  # #54 6a / 7a
        assert "Please enter a project title." in post(designer, "/designer/portfolio/current/2/edit",
                                                       **{**GOOD, "title": ""})
        assert "could not be saved" in post(designer, "/designer/portfolio/current/3/edit", **GOOD)

    def test_edit_past_future_date(self, designer):                        # #59 6a
        html = post(designer, "/designer/portfolio/past/1/edit", **GOOD, completionDate=TOMORROW)
        assert "cannot be in the future" in html

    def test_delete_has_confirmation_popup(self, designer):                # #55 / #60 steps 2-3
        html = designer.get("/designer/portfolio").get_data(as_text=True)
        assert 'id="delete-2"' in html and 'href="#">Cancel</a>' in html

    def test_delete(self, designer):                                       # #55 steps 4-5
        html = post(designer, "/designer/portfolio/current/2/delete")
        assert "deleted from your portfolio" in html and InteriorDesignProject.findIDPByID(2) == {}

    def test_delete_failed(self, designer):                                # #60 4a
        assert "could not be deleted" in post(designer, "/designer/portfolio/past/2/delete")

    def test_search_and_no_results(self, designer):                        # #56 / #61
        assert "Sengkang" in designer.get("/designer/portfolio?kind=current&q=fluted").get_data(as_text=True)
        assert "No matching results were found" in \
            designer.get("/designer/portfolio?kind=past&q=castle").get_data(as_text=True)

    def test_customer_finds_new_project(self, designer):                   # works with #32
        post(designer, "/designer/portfolio/create/past", **GOOD, completionDate="2026-05-01")
        customer = loggedIn(app_module, "customer@4reno.com", "password123")
        assert "Bedok Condo Study" in customer.get("/search?keyword=bedok&category=").get_data(as_text=True)

    def test_only_designers(self):                                         # precondition
        customer = loggedIn(app_module, "customer@4reno.com", "password123")
        assert customer.get("/designer/portfolio").status_code == 302

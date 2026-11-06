"""
Unit tests for #65 Create, #66 Update, #67 View, #68 Delete and #69 Search IDP categories
(Platform Administrator), and the portfolio form's category choice.
Run from the project folder:   python -m pytest tests/test_idp_categories.py -v
"""
import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import IDPCategory, InteriorDesignProject                       # noqa: E402
from control import (CreateIDPCategoryController, UpdateIDPCategoryController,   # noqa: E402
                     ViewIDPCategoryController, DeleteIDPCategoryController,
                     SearchIDPCategoryController)
from boundary.idp_category_page import validateCategoryForm, validateProjectChoice   # noqa: E402
from boundary.portfolio_forms import validateForm                           # noqa: E402
from tests.helpers import loggedIn, post                                    # noqa: E402


@pytest.fixture(autouse=True)
def fresh_data():
    saved = (copy.deepcopy(IDPCategory._categories), IDPCategory._nextID, list(InteriorDesignProject._idps))
    IDPCategory._categories, IDPCategory._nextID = [], 1
    IDPCategory.createCategory("Kitchen", "Kitchens and pantries")       # IDP-CAT-001
    IDPCategory.createCategory("Bedroom", "")                            # IDP-CAT-002
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, "d@4reno.com", "Punggol Kitchen", "2026-09-02", category="Kitchen"),
        InteriorDesignProject(2, "d@4reno.com", "Clementi Bedroom", "2026-10-19", category="Bedroom"),
        InteriorDesignProject(3, "d@4reno.com", "Tampines Kitchen", "2026-08-14", category="Kitchen"),
    ]
    yield
    IDPCategory._categories, IDPCategory._nextID, InteriorDesignProject._idps = saved


@pytest.fixture
def platform():
    app_module.app.config["TESTING"] = True
    return loggedIn(app_module, "platform@4reno.com", "platform123")


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_names_unique_case_insensitive(self):                         # #65 / #66
        assert IDPCategory.nameExists("KITCHEN") is True
        assert IDPCategory.nameExists("Kitchen", "IDP-CAT-001") is False   # its own name on update

    def test_create_returns_id(self):                                      # #65
        assert IDPCategory.createCategory("Study", "") == "IDP-CAT-003"
        assert IDPCategory.getCategoryNames() == ["Bedroom", "Kitchen", "Study"]

    def test_search_name_or_description(self):                             # #69
        assert [c["name"] for c in IDPCategory.searchCategories("pantr")] == ["Kitchen"]
        assert IDPCategory.searchCategories("garage") == []

    def test_project_category_methods(self):
        assert [p["name"] for p in InteriorDesignProject.getProjectsInCategory("kitchen")] == \
            ["Punggol Kitchen", "Tampines Kitchen"]
        assert InteriorDesignProject.renameCategory("Kitchen", "Cooking") == 2
        assert InteriorDesignProject.setProjectCategory(999, "Kitchen") is False


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_list_has_project_counts(self):                                # #67
        counts = {c["name"]: c["projectCount"] for c in ViewIDPCategoryController().getCategoryList()}
        assert counts == {"Bedroom": 1, "Kitchen": 2}

    def test_create_links_projects(self):                                  # #65
        categoryID = CreateIDPCategoryController().createCategory("Bathroom", "", [2])
        assert [p["name"] for p in ViewIDPCategoryController().getCategory(categoryID)["projects"]] == ["Clementi Bedroom"]

    def test_rename_keeps_projects(self):                                  # #66
        assert UpdateIDPCategoryController().updateCategory("IDP-CAT-001", "Cooking", "x") is True
        assert ViewIDPCategoryController().getCategory("IDP-CAT-001")["projectCount"] == 2

    def test_assign_moves_project(self):                                   # #66
        assert UpdateIDPCategoryController().assignProject("IDP-CAT-002", 1) is True
        assert ViewIDPCategoryController().getCategory("IDP-CAT-001")["projectCount"] == 1

    def test_delete(self):                                                 # #68
        IDPCategory.createCategory("Garage", "")
        assert DeleteIDPCategoryController().deleteCategory("IDP-CAT-003") is True
        assert ViewIDPCategoryController().getCategory("IDP-CAT-003") == {}

    def test_search_projects_in_category(self):                            # #69
        assert [p["name"] for p in SearchIDPCategoryController().searchProjectsInCategory("IDP-CAT-001", "punggol")] \
            == ["Punggol Kitchen"]


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_category_form(self):
        assert validateCategoryForm({"name": "Study", "description": ""}) == {}
        assert set(validateCategoryForm({"name": "", "description": "d" * 501})) == {"name", "description"}
        assert "name" in validateCategoryForm({"name": "n" * 81, "description": ""})

    def test_project_choice(self):
        projects = [{"projectID": 1}, {"projectID": 2}]
        assert validateProjectChoice(["1"], projects) == ""
        assert validateProjectChoice(["1", "1"], projects) != ""
        assert validateProjectChoice(["9"], projects) != ""

    def test_portfolio_category_must_be_managed(self):
        form = {"title": "t", "description": "d", "designs": "d", "materials": "m", "category": "Pool",
                "completionDate": ""}
        assert "category" in validateForm(form, "current", ["Kitchen"])
        assert validateForm({**form, "category": "Kitchen"}, "current", ["Kitchen"]) == {}


# ---------------------------------------------------------------- Boundary pages
class TestPages:
    def test_list(self, platform):                                         # #67
        html = platform.get("/platform/idp-categories").get_data(as_text=True)
        assert "Kitchen" in html and "Bedroom" in html

    def test_create_and_duplicate(self, platform):                         # #65
        assert 'was created' in post(platform, "/platform/idp-categories/create", name="Study", description="")
        assert "already taken" in post(platform, "/platform/idp-categories/create", name="study", description="")

    def test_view(self, platform):                                         # #67
        html = platform.get("/platform/idp-categories/IDP-CAT-001").get_data(as_text=True)
        assert "Punggol Kitchen" in html and "Tampines Kitchen" in html
        assert platform.get("/platform/idp-categories/IDP-CAT-999").status_code == 404

    def test_update(self, platform):                                       # #66
        html = post(platform, "/platform/idp-categories/IDP-CAT-001/update", name="Kitchen & Dining", description="")
        assert "was updated" in html and "Punggol Kitchen" in html

    def test_delete_blocked_then_allowed(self, platform):                  # #68
        assert "still has 2 linked project(s)" in post(platform, "/platform/idp-categories/IDP-CAT-001/delete")
        IDPCategory.createCategory("Garage", "")
        assert "was deleted" in post(platform, "/platform/idp-categories/IDP-CAT-003/delete")

    def test_search(self, platform):                                       # #69
        html = platform.get("/platform/idp-categories/search?keyword=pantr").get_data(as_text=True)
        assert "Kitchen" in html and "Bedroom</a>" not in html
        assert "No categories found" in platform.get("/platform/idp-categories/search?keyword=zzz").get_data(as_text=True)

    def test_only_platform_admin(self):                                    # precondition
        designer = loggedIn(app_module, "designer@4reno.com", "design123")
        assert designer.get("/platform/idp-categories").status_code == 302

"""«Boundary» IDPCategoryPage — #65 Create, #66 Update, #67 View, #68 Delete, #69 Search IDP categories
(no class: idp_categories.html, idp_category_form.html, idp_category_details.html + route functions).
Precondition (logged-in Platform Administrator) is enforced by requirePlatform() in app.py."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort

from control import (CreateIDPCategoryController, UpdateIDPCategoryController, ViewIDPCategoryController,
                     DeleteIDPCategoryController, SearchIDPCategoryController)

idp_category_management = Blueprint("idp_category_management", __name__)

MAX_NAME_LENGTH = 80
MAX_DESCRIPTION_LENGTH = 500
MAX_SEARCH_LENGTH = 100
NAME_TAKEN = "That category name is already taken. Choose a unique name."


# ---- shared Boundary helpers -------------------------------------------------
def displayCategoryList(categories: list, keyword: str = "", searched: bool = False,
                        selectedCategory: dict = None, projects: list = None,
                        projectKeyword: str = "", error: str = "") -> str:
    # An empty list after a search shows "No categories found" (#69) in the template
    return render_template("idp_categories.html", categories=categories, keyword=keyword,
                           searched=searched, selectedCategory=selectedCategory or {},
                           projects=projects or [], projectKeyword=projectKeyword, error=error,
                           active="categories")


def displayCategoryForm(mode: str, controller, form: dict, errors: dict = None,
                        category: dict = None) -> str:
    return render_template("idp_category_form.html", mode=mode, form=form, errors=errors or {},
                           category=category or {}, projects=controller.getProjects(),
                           active="categories")


def displayCategoryDetails(category: dict, projects: list, errors: dict = None) -> str:   # #67
    # Projects that could be moved into this category (#66 assign)
    assignable = [p for p in ViewIDPCategoryController().getProjects() if p["category"] != category["name"]]
    return render_template("idp_category_details.html", category=category, errors=errors or {},
                           projects=projects, assignable=assignable, active="categories")


def readCategoryForm() -> dict:
    return {"name": request.form.get("name", "").strip(),
            "description": request.form.get("description", "").strip()}


def validateCategoryForm(form: dict) -> dict:
    """Boundary input check for #65 / #66: a name, and both fields within their limits.
    Returns errors; {} = valid."""
    errors = {}
    if not form["name"]:
        errors["name"] = "Enter a category name."
    elif len(form["name"]) > MAX_NAME_LENGTH:
        errors["name"] = f"Category name must be {MAX_NAME_LENGTH} characters or fewer."
    if len(form["description"]) > MAX_DESCRIPTION_LENGTH:
        errors["description"] = f"Description must be {MAX_DESCRIPTION_LENGTH} characters or fewer."
    return errors


def validateProjectChoice(chosen: list, projects: list) -> str:
    """Boundary input check: every chosen project is one from the list, chosen once."""
    available = {str(p["projectID"]) for p in projects}
    if len(chosen) != len(set(chosen)):
        return "A project can only be selected once."
    if any(c not in available for c in chosen):
        return "Select an available project."
    return ""


# ---- #67 / #69: category list ----------------------------------------------
@idp_category_management.get("/platform/idp-categories")
def categoryListPage() -> str:
    # Platform Administrator opens IDP Categories: every category with its project count
    return displayCategoryList(ViewIDPCategoryController().getCategoryList())


# ---- #65 Create --------------------------------------------------------------
@idp_category_management.route("/platform/idp-categories/create", methods=["GET", "POST"])
def createCategoryPage() -> str:
    controller = CreateIDPCategoryController()
    if request.method == "GET":
        return displayCategoryForm("create", controller, {"projectIDs": []})

    form = {**readCategoryForm(), "projectIDs": [v.strip() for v in request.form.getlist("projectIDs") if v.strip()]}
    errors = validateCategoryForm(form)
    projectError = validateProjectChoice(form["projectIDs"], controller.getProjects())
    if projectError:
        errors["projects"] = projectError
    if not errors and controller.categoryExists(form["name"]):          # stored data -> via Control
        errors["name"] = NAME_TAKEN
    if errors:
        return displayCategoryForm("create", controller, form, errors)

    controller.createCategory(form["name"], form["description"], [int(i) for i in form["projectIDs"]])
    flash(f'Category "{form["name"]}" was created.', "ok")
    return redirect(url_for("idp_category_management.categoryListPage"))


# ---- #66 Update --------------------------------------------------------------
@idp_category_management.route("/platform/idp-categories/<categoryID>/update", methods=["GET", "POST"])
def updateCategoryPage(categoryID: str) -> str:
    controller = UpdateIDPCategoryController()
    category = controller.getCategory(categoryID)
    if not category:                                                     # precondition: it exists
        abort(404)
    if request.method == "GET":
        return displayCategoryForm("update", controller, category, category=category)

    form = readCategoryForm()
    errors = validateCategoryForm(form)
    if not errors and controller.categoryExists(form["name"], categoryID):
        errors["name"] = NAME_TAKEN
    if errors:
        return displayCategoryForm("update", controller, form, errors, category)

    controller.updateCategory(categoryID, form["name"], form["description"])
    flash(f'Category "{form["name"]}" was updated.', "ok")
    return redirect(url_for("idp_category_management.viewCategoryPage", categoryID=categoryID))


@idp_category_management.post("/platform/idp-categories/<categoryID>/assign-project")
def assignProjectPage(categoryID: str) -> str:
    """#66: link a project to this category (or move it here from another one)."""
    controller = UpdateIDPCategoryController()
    category = controller.getCategory(categoryID)
    if not category:
        abort(404)
    projectID = request.form.get("projectID", "").strip()
    error = validateProjectChoice([projectID], controller.getProjects())
    if error:
        return displayCategoryDetails(category, category["projects"], {"projectID": error})
    controller.assignProject(categoryID, int(projectID))
    flash("The project was assigned to this category.", "ok")
    return redirect(url_for("idp_category_management.viewCategoryPage", categoryID=categoryID))


# ---- #69 Search --------------------------------------------------------------
@idp_category_management.get("/platform/idp-categories/search")
def searchCategoryPage() -> str:
    keyword = request.args.get("keyword", "").strip()
    projectKeyword = request.args.get("projectKeyword", "").strip()
    categoryID = request.args.get("categoryID", "").strip()
    # Boundary checks the search text
    if len(keyword) > MAX_SEARCH_LENGTH or len(projectKeyword) > MAX_SEARCH_LENGTH:
        return displayCategoryList([], keyword, True, projectKeyword=projectKeyword,
                                   error=f"Search text must be {MAX_SEARCH_LENGTH} characters or fewer.")
    controller = SearchIDPCategoryController()
    # Search categories by name or description, then (optionally) projects inside one category
    categories = controller.searchCategories(keyword)
    selectedCategory = controller.getCategory(categoryID) if categoryID else {}
    projects = controller.searchProjectsInCategory(categoryID, projectKeyword) if selectedCategory else []
    return displayCategoryList(categories, keyword, True, selectedCategory, projects, projectKeyword)


# ---- #67 View ----------------------------------------------------------------
@idp_category_management.get("/platform/idp-categories/<categoryID>")
def viewCategoryPage(categoryID: str) -> str:
    # Platform Administrator selects a category: its details and linked projects
    category = ViewIDPCategoryController().getCategory(categoryID)
    if not category:
        abort(404)
    return displayCategoryDetails(category, category["projects"])


# ---- #68 Delete --------------------------------------------------------------
@idp_category_management.post("/platform/idp-categories/<categoryID>/delete")
def deleteCategoryPage(categoryID: str) -> str:
    # Platform Administrator confirmed Delete in the pop-up
    controller = DeleteIDPCategoryController()
    category = controller.getCategory(categoryID)
    if not category:
        abort(404)
    linkedCount = category["projectCount"]
    if linkedCount:                                                      # blocked while projects remain
        flash(f"This category still has {linkedCount} linked project(s). Reassign them before deleting it.", "err")
        return redirect(url_for("idp_category_management.viewCategoryPage", categoryID=categoryID))
    controller.deleteCategory(categoryID)
    flash(f'Category "{category["name"]}" was deleted.', "ok")
    return redirect(url_for("idp_category_management.categoryListPage"))

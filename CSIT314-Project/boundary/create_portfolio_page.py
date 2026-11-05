"""«Boundary» CreatePortfolioPage — #52 Create current project / #57 Create past project
(no class: portfolio_form.html + route functions)."""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from control import CreateCurrentProjectController, CreatePastProjectController
from boundary.portfolio_forms import KIND_LABELS, readPortfolioForm, validateForm

create_portfolio = Blueprint("create_portfolio", __name__)

CONTROLLERS = {"current": CreateCurrentProjectController, "past": CreatePastProjectController}


def displayCreateForm(kind: str, form: dict = None, fieldErrors: dict = None) -> str:   # step 2
    return render_template("portfolio_form.html", mode="create", kind=kind, kindLabels=KIND_LABELS,
                           form=form or {}, fieldErrors=fieldErrors or {},
                           categories=CONTROLLERS[kind]().getCategories(), active="portfolio")


def displayError(kind: str, form: dict, fieldErrors: dict) -> str:     # 5a
    return displayCreateForm(kind, form, fieldErrors)


def displaySuccess(kind: str) -> str:                                   # step 7
    flash(f"Portfolio for your {KIND_LABELS[kind].lower()} was created successfully.", "ok")
    return redirect(url_for("portfolio.portfolioPage", kind=kind))


def submitDetails(kind: str, form: dict) -> str:
    # Step 5: Boundary validates the entered information
    fieldErrors = validateForm(form, kind, CONTROLLERS[kind]().getCategories())
    if fieldErrors:
        return displayError(kind, form, fieldErrors)
    # Step 6: save the project with status "Current" (#52) or "Past" (#57)
    CONTROLLERS[kind]().createProject(session["u"], form["title"], form["description"], form["designs"],
                                      form["materials"], form["category"], form["completionDate"])
    return displaySuccess(kind)


@create_portfolio.route("/designer/portfolio/create/<any(current, past):kind>", methods=["GET", "POST"])
def openCreatePage(kind: str) -> str:
    # Step 1: ID clicks "Create Portfolio" and selects Current Project / Past Project
    if request.method == "GET":
        return displayCreateForm(kind)
    # Steps 3-4: ID entered the project details and submitted
    return submitDetails(kind, readPortfolioForm(kind))

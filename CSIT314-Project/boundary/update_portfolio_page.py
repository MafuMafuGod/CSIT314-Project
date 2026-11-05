"""«Boundary» UpdatePortfolioPage — #54 Update current project / #59 Update past project
(no class: portfolio_form.html + route functions)."""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from control import UpdateCurrentProjectController, UpdatePastProjectController
from boundary.portfolio_forms import KIND_LABELS, readPortfolioForm, validateForm

update_portfolio = Blueprint("update_portfolio", __name__)

CONTROLLERS = {"current": UpdateCurrentProjectController, "past": UpdatePastProjectController}


def displayEditForm(kind: str, idpID: int, form: dict, fieldErrors: dict = None,
                    error: str = None) -> str:                           # step 3
    return render_template("portfolio_form.html", mode="update", kind=kind, idpID=idpID,
                           kindLabels=KIND_LABELS, form=form, fieldErrors=fieldErrors or {},
                           error=error, categories=CONTROLLERS[kind]().getCategories(),
                           active="portfolio")


def displaySuccess(kind: str, idpID: int) -> str:                       # step 8
    flash("Portfolio updated successfully.", "ok")
    return redirect(url_for("view_portfolio.viewProjectPage", kind=kind, idpID=idpID))


def displayNotFound(kind: str) -> str:                                  # precondition failed
    flash("This project's portfolio information is unavailable.", "err")
    return redirect(url_for("portfolio.portfolioPage", kind=kind))


def submitChanges(kind: str, idpID: int, form: dict) -> str:
    # Step 6: Boundary validates the updated information
    fieldErrors = validateForm(form, kind, CONTROLLERS[kind]().getCategories())
    if fieldErrors:                                                     # 6a
        return displayEditForm(kind, idpID, form, fieldErrors)
    # Step 7: save the updated portfolio
    updated = CONTROLLERS[kind]().updateProject(session["u"], idpID, form["title"], form["description"],
                                                form["designs"], form["materials"], form["category"],
                                                form["completionDate"])
    if not updated:                                                     # 7a
        return displayEditForm(kind, idpID, form, error="The changes could not be saved. Please try again.")
    return displaySuccess(kind, idpID)


@update_portfolio.route("/designer/portfolio/<any(current, past):kind>/<int:idpID>/edit",
                        methods=["GET", "POST"])
def editProjectPage(kind: str, idpID: int) -> str:
    if request.method == "POST":
        # Steps 4-5: ID modified the fields and clicked Save
        return submitChanges(kind, idpID, readPortfolioForm(kind))
    # Step 1: ID clicks Edit; step 2: retrieve the existing portfolio information
    project = CONTROLLERS[kind]().getProject(session["u"], idpID)
    if not project:
        return displayNotFound(kind)
    return displayEditForm(kind, idpID, project)

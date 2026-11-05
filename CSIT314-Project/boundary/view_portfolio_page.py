"""«Boundary» ViewPortfolioPage — #53 View current project / #58 View past project"""
from flask import Blueprint, render_template, session

from control import ViewCurrentProjectController, ViewPastProjectController
from boundary.portfolio_forms import KIND_LABELS

view_portfolio = Blueprint("view_portfolio", __name__)

CONTROLLERS = {"current": ViewCurrentProjectController, "past": ViewPastProjectController}


def displayProject(kind: str, project: dict) -> str:                    # #53 step 4 / #58 step 3
    return render_template("portfolio_view.html", kind=kind, kindLabels=KIND_LABELS,
                           project=project, active="portfolio")


def displayUnavailable(kind: str) -> str:                               # #53 3a / #58 2a
    return render_template("portfolio_view.html", kind=kind, kindLabels=KIND_LABELS, project=None,
                           error="This project's portfolio information is unavailable.",
                           active="portfolio")


@view_portfolio.route("/designer/portfolio/<any(current, past):kind>/<int:idpID>")
def viewProjectPage(kind: str, idpID: int) -> str:
    # #53 step 2 / #58 step 1: ID selects the project to view
    # #53 step 3 / #58 step 2: retrieve its portfolio information
    project = CONTROLLERS[kind]().getProject(session["u"], idpID)
    if not project:
        return displayUnavailable(kind)
    return displayProject(kind, project)

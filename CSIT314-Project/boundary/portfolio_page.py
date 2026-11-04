"""«Boundary» PortfolioManagementPage — the portfolio management page
(no class: portfolio.html + route functions).
  #53 step 1 / #58 step 1: lists the ID's current or past projects
  #56 / #61: searches them by keyword (4a: "No matching results were found")"""
from flask import Blueprint, render_template, request, session, flash

from control import (ViewCurrentProjectController, ViewPastProjectController,
                     SearchCurrentProjectController, SearchPastProjectController)
from boundary.portfolio_forms import KIND_LABELS

portfolio = Blueprint("portfolio", __name__)

LIST_CONTROLLERS = {"current": ViewCurrentProjectController, "past": ViewPastProjectController}
SEARCH_CONTROLLERS = {"current": SearchCurrentProjectController, "past": SearchPastProjectController}
MAX_KEYWORD_LENGTH = 100


def displayPortfolioPage(kind: str, projects: list, keyword: str = "", searched: bool = False) -> str:
    return render_template("portfolio.html", kind=kind, kindLabels=KIND_LABELS, projects=projects,
                           keyword=keyword, searched=searched, active="portfolio")


def validateKeyword(keyword: str) -> str:                               # #56 / #61 step 2
    """Boundary input check. Returns an error message, "" = valid."""
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return f"Keyword must be {MAX_KEYWORD_LENGTH} characters or fewer."
    return ""


def submitSearch(designerU: str, kind: str, keyword: str) -> str:
    # #56 / #61 step 2: Boundary checks the keyword
    error = validateKeyword(keyword)
    if error:
        flash(error, "err")
        return displayPortfolioPage(kind, [], keyword, searched=True)
    # Step 3: search the ID's current / past projects
    matchingProjects = SEARCH_CONTROLLERS[kind]().searchProjects(designerU, keyword)
    # Step 4: display the results (4a: empty list -> "No matching results were found")
    return displayPortfolioPage(kind, matchingProjects, keyword, searched=True)


@portfolio.route("/designer/portfolio")
def portfolioPage() -> str:
    designerU = session["u"]
    kind = request.args.get("kind", "current")
    if kind not in KIND_LABELS:
        kind = "current"
    keyword = request.args.get("q", "").strip()
    if keyword:
        # #56 / #61 step 1: ID entered a keyword and clicked Search
        return submitSearch(designerU, kind, keyword)
    # #53 / #58 step 1: the system displays the ID's current or past projects
    return displayPortfolioPage(kind, LIST_CONTROLLERS[kind]().getProjectList(designerU))

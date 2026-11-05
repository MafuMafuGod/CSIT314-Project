"""«Boundary» SearchCompanyProfilesPage — #13 Search company profiles
(no class: search_company_profiles.html + route function).
Precondition (logged-in Interior Designer) is enforced by requireDesigner() in app.py."""
from flask import Blueprint, render_template, request

from control import SearchCompanyProfilesController

search_company_profiles = Blueprint("search_company_profiles", __name__)

MAX_KEYWORD_LENGTH = 100


def displaySearchPage(keyword: str = "", results: list = None, searched: bool = False,
                      error: str = None) -> str:
    # An empty list after a search shows "No matching company profiles were found"
    return render_template("search_company_profiles.html", keyword=keyword, results=results or [],
                           searched=searched, error=error, active="company_search")


def validateKeyword(keyword: str) -> str:
    """Boundary input check. Returns an error message, "" = valid."""
    if not keyword:
        return "Enter a company name or keyword to search."
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return f"Search text must be {MAX_KEYWORD_LENGTH} characters or fewer."
    return ""


@search_company_profiles.route("/designer/company-profiles/search")
def searchCompanyProfiles() -> str:
    if "keyword" not in request.args:
        # ID opens Search Company Profiles: show the search box
        return displaySearchPage()
    # ID entered a company name or keyword and clicked Search
    keyword = request.args.get("keyword", "").strip()
    error = validateKeyword(keyword)
    if error:
        return displaySearchPage(keyword, searched=True, error=error)
    results = SearchCompanyProfilesController().searchCompanyProfiles(keyword)
    return displaySearchPage(keyword, results, searched=True)

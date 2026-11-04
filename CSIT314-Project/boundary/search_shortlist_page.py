"""«Boundary» SearchShortlistPage — #35 Search Shortlist (no class: shortlist.html + route functions).
Opening the page lists every saved IDP, so the Customer can pick one to view (#36 step 1-2)."""
from flask import Blueprint, render_template, request, session

from control import SearchShortlistController

search_shortlist = Blueprint("search_shortlist", __name__)

MAX_KEYWORD_LENGTH = 100


def displayShortlistPage(keyword: str = "", error: str = None, emptyShortlist: bool = False,
                         searched: bool = False, idpList: list = None) -> str:
    return render_template("shortlist.html", keyword=keyword, error=error,
                           emptyShortlist=emptyShortlist, searched=searched,
                           results=idpList or [], active="shortlist")


def validateKeyword(keyword: str) -> str:                               # step 3
    """Boundary input check. Returns an error message, "" = valid."""
    if not keyword:                                                     # 3a
        return "Please enter a keyword to search your Shortlist."
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return f"Keyword must be {MAX_KEYWORD_LENGTH} characters or fewer."
    return ""


def displayError(keyword: str, error: str) -> str:                      # 3a
    return displayShortlistPage(keyword, error=error)


def displayEmptyShortlist() -> str:                                     # 5a
    return displayShortlistPage(emptyShortlist=True)


def displayResults(keyword: str, idpList: list) -> str:                # step 7 / 6a
    # An empty list shows "No matching saved projects were found" (6a) in the template
    return displayShortlistPage(keyword, searched=True, idpList=idpList)


def submitSearch(customerU: str, keyword: str) -> str:
    # Step 3: Boundary validates the search input
    error = validateKeyword(keyword)
    if error:
        return displayError(keyword, error)

    controller = SearchShortlistController()
    # Step 5: retrieve the Customer's saved IDPs
    savedIDPs = controller.getSavedIDPs(customerU)
    if not savedIDPs:
        return displayEmptyShortlist()
    # Step 6: filter them by the keyword; step 7: display
    return displayResults(keyword, controller.searchShortlist(customerU, keyword))


@search_shortlist.route("/shortlist")
def shortlistPage() -> str:
    customerU = session["u"]
    if "keyword" in request.args:
        # Steps 3-4: Customer entered a keyword and submitted
        return submitSearch(customerU, request.args.get("keyword", "").strip())
    # Steps 1-2: Customer opens the Shortlist; the search box and all saved IDPs are shown
    savedIDPs = SearchShortlistController().getSavedIDPs(customerU)
    if not savedIDPs:
        return displayEmptyShortlist()                                  # 5a
    return displayResults("", savedIDPs)

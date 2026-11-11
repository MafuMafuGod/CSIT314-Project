"""«Boundary» 
SearchShortlistPage — #35 Search Shortlist (no class: shortlist.html + route functions)
Opening the page lists every saved IDP, so the Customer can pick one to view (#36 step 1-2)"""
from flask import Blueprint, render_template, request, session

from control import SearchShortlistController

search_shortlist = Blueprint("search_shortlist", __name__)

MAX_KEYWORD_LENGTH = 100

# emptyShortlist = nothing saved yet, searched = a search was done
def displayShortlistPage(keyword: str = "", error: str = None, emptyShortlist: bool = False,
                         searched: bool = False, idpList: list = None) -> str:
    return render_template("shortlist.html", keyword=keyword, error=error,
                           emptyShortlist=emptyShortlist, searched=searched,
                           results=idpList or [], active="shortlist")

# Checks the keyword. Returns an error message, or "" when it is fine
def validateKeyword(keyword: str) -> str:                               # step 3
    """Boundary input check. Returns an error message, "" = valid."""
    # nothing typed
    if not keyword:                                                     # 3a
        return "Please enter a keyword to search your Shortlist."
    # keyword is too long
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return f"Keyword must be {MAX_KEYWORD_LENGTH} characters or fewer."
    return ""

# Shows the page again with an error message
def displayError(keyword: str, error: str) -> str:                      # 3a
    return displayShortlistPage(keyword, error=error)

# Shows the "Your Shortlist is empty" message
def displayEmptyShortlist() -> str:                                     # 5a
    return displayShortlistPage(emptyShortlist=True)

# Shows the saved projects that match
def displayResults(keyword: str, idpList: list) -> str:                # step 7 / 6a
    # An empty list shows "No matching saved projects were found" (6a) 
    return displayShortlistPage(keyword, searched=True, idpList=idpList)

# Runs the search steps in order: check keyword, get saved IDPs, filter, show
def submitSearch(customerU: str, keyword: str) -> str:
    # Step 3: Boundary validates the search input
    error = validateKeyword(keyword)
    if error:
        return displayError(keyword, error)

    controller = SearchShortlistController()
    # Step 5: retrieve the Customer's saved IDPs
    # all the IDPs this Customer has saved
    savedIDPs = controller.getSavedIDPs(customerU)
    # nothing saved yet
    if not savedIDPs:
        return displayEmptyShortlist()
    # Step 6: filter them by the keyword; step 7: display
    return displayResults(keyword, controller.searchShortlist(customerU, keyword))


@search_shortlist.route("/shortlist")
def shortlistPage() -> str:
    # the logged-in Customer's email (saved in the session at login)
    customerU = session["u"]
    # a keyword in the address = the search form was sent
    if "keyword" in request.args:
        # Steps 3-4: Customer entered a keyword and submitted
        return submitSearch(customerU, request.args.get("keyword", "").strip())
    # Steps 1-2: Customer opens the Shortlist; the search box and all saved IDPs are shown
    savedIDPs = SearchShortlistController().getSavedIDPs(customerU)
    if not savedIDPs:
        return displayEmptyShortlist()                                  # 5a
    return displayResults("", savedIDPs)

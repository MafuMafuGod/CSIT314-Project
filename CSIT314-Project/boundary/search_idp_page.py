"""«Boundary» SearchIDPPage — #32 Search IDPs (no class: idp_search.html + route functions).
An empty result list is handled by idp_search.html itself (6a: "No matching IDPs were found")."""
from flask import Blueprint, render_template, request

from control import SearchIDPController

search_idp = Blueprint("search_idp", __name__)

MAX_KEYWORD_LENGTH = 100

# searched = True means a search was done -> page shows the results or "No matching IDPs"
def displaySearchPage(categories: list, keyword: str = "", category: str = "",
                      error: str = None, searched: bool = False, idpList: list = None) -> str:
    # render_template fills idp_search.html with these values
    return render_template("idp_search.html", categories=categories, keyword=keyword,
                           category=category, error=error, searched=searched,
                           results=idpList or [], active="search")

# Checks the search input. Returns an error message, or "" when the input is fine
def validateSearch(keyword: str, category: str, categories: list) -> str:
    """Step 5: Boundary input check. Returns an error message, "" = valid."""
    # nothing typed and no category chosen
    if not keyword and not category:                                     # 31 (5a)
        return "Please enter a keyword or select a category."
    # keyword is too long
    if len(keyword) > MAX_KEYWORD_LENGTH:
        return f"Keyword must be {MAX_KEYWORD_LENGTH} characters or fewer."
    # the category is not one of the real categories
    if category and category not in categories:
        return "Please select a category from the list."
    return ""

# Shows the search page again with an error message
def displayError(categories: list, keyword: str, category: str, error: str) -> str:   # 31 (5a)
    return displaySearchPage(categories, keyword, category, error=error)

# Shows the search page with the results (an empty list shows "No matching IDPs")
def displayResults(categories: list, keyword: str, category: str, idpList: list) -> str:  # step 7 / 6a
    return displaySearchPage(categories, keyword, category, searched=True, idpList=idpList)

# Runs the search steps in order: get categories, check input, search, show results
def submitSearch(keyword: str, category: str) -> str:
    controller = SearchIDPController()
    categories = controller.getCategories()

    # Step 5: Boundary validates the search input
    error = validateSearch(keyword, category, categories)
    if error:
        return displayError(categories, keyword, category, error)

    # Step 6: retrieve the matching IDPs
    idpList = controller.searchIDPs(keyword, category)
    # Step 7: display them (empty list shows the "no matching IDPs" message)
    return displayResults(categories, keyword, category, idpList)

# The page address is /search. The search words are in the address, e.g. /search?keyword=hdb&category=Kitchen
@search_idp.route("/search")
def searchPage() -> str:
    # Step 1: Customer opens the Search IDPs page (no search submitted yet)
    # no search words in the address = the page was just opened
    if "keyword" not in request.args and "category" not in request.args:
        # Step 2: display the search form
        return displaySearchPage(SearchIDPController().getCategories())
    # Steps 3-4: Customer entered a keyword and/or category and submitted
    return submitSearch(request.args.get("keyword", "").strip(),
                        request.args.get("category", "").strip())

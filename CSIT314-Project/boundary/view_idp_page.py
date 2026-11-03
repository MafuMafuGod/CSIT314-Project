"""«Boundary» ViewIDPPage — #33 View IDP Details (no class: idp_details.html + route functions).
The idpID comes from the URL; Flask's <int:idpID> already rejects anything that is not a
number, so there is no typed input left for the Boundary to validate."""
from urllib.parse import urlparse

from flask import Blueprint, render_template, request, url_for

from control import ViewIDPController

view_idp = Blueprint("view_idp", __name__)


def getBackUrl() -> str:
    """Step 5: link back to the list the Customer came from (search results, home),
    or the search page if they arrived some other way."""
    referrer = request.referrer or ""
    if referrer and urlparse(referrer).netloc == request.host and "/idp/" not in referrer:
        return referrer
    return url_for("search_idp.searchPage")


def displayIDPDetails(idp: dict) -> str:                                # step 4
    return render_template("idp_details.html", idp=idp, error=None,
                           backUrl=getBackUrl(), active="search")


def displayError(message: str) -> str:                                  # 3a
    return render_template("idp_details.html", idp=None, error=message,
                           backUrl=getBackUrl(), active="search")


@view_idp.route("/idp/<int:idpID>")
def viewIdpPage(idpID: int) -> str:
    # Steps 1-2: Customer selects an IDP from a list
    # Step 3: retrieve the selected IDP's details
    idp = ViewIDPController().viewIDPDetails(idpID)
    if not idp:
        return displayError("Sorry, this IDP could not be found. It may have been removed.")   # [else] 3a
    return displayIDPDetails(idp)                                       # [idp found] step 4

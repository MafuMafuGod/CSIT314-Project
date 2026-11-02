"""«Boundary» IDPInterestPage — #40 / #41 (Matthew)
(no class: interest.html + route functions).
An empty list is handled by interest.html itself, so no separate "no IDP found" branch."""
from flask import Blueprint, render_template, session

from control import ViewIDPViewCountController, ViewIDPShortlistCountController

idp_interest = Blueprint("idp_interest", __name__)


def displayIDPInterest(tab: str, rows: list) -> str:                    # step 3
    return render_template("interest.html", tab=tab, rows=rows, active="interest")


@idp_interest.route("/designer/interest")
@idp_interest.route("/designer/interest/views")
def viewCountPage() -> str:
    # #40 Step 1: ID clicks "IDP Interest" in the navigation bar
    u = session["u"]
    # Step 2: retrieve all the ID's IDPs with their view counts
    idpViewCounts = ViewIDPViewCountController().getViewCounts(u)
    # Step 3: display them (empty list shows the "no IDPs" message in the template)
    return displayIDPInterest("views", idpViewCounts)


@idp_interest.route("/designer/interest/shortlists")
def shortlistCountPage() -> str:
    # #41 Step 1: ID clicks "IDP Interest", then the "Shortlisted" tab
    u = session["u"]
    # Step 2: retrieve all the ID's IDPs with their shortlist counts
    idpShortlistCounts = ViewIDPShortlistCountController().getShortlistCounts(u)
    # Step 3: display them (empty list shows the "no IDPs" message in the template)
    return displayIDPInterest("shortlists", idpShortlistCounts)

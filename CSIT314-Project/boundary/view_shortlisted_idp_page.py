"""«Boundary» 
ViewShortlistedIDPPage — #36 View Shortlisted IDP
(no class: shortlist_view.html + route functions)
The idpID comes from the URL (<int:idpID>), so there is no typed input to validate"""
from flask import Blueprint, render_template, session

from control import ViewShortlistedIDPController

view_shortlisted = Blueprint("view_shortlisted", __name__)

# Shows the details of one saved project
def displayIDPDetails(idp: dict) -> str:                                # step 6
    return render_template("shortlist_view.html", idp=idp, active="shortlist")

# Shows a message instead of the project. kind sets the colour: info = blue, err = red
def displayMessage(message: str, kind: str) -> str:                     # 4a / 5a
    return render_template("shortlist_view.html", idp=None, message=message, kind=kind,
                           active="shortlist")

# <int:idpID> takes the number from the address, e.g. /shortlist/2 gives idpID = 2
@view_shortlisted.route("/shortlist/<int:idpID>")
def viewShortlistedPage(idpID: int) -> str:
    # Step 3: Customer selects a project from their Shortlist
    controller = ViewShortlistedIDPController()

    # Step 4: is it in the Customer's Shortlist?
    # session["u"] = the logged-in Customer's email
    inShortlist = controller.isInShortlist(session["u"], idpID)
    if not inShortlist:                                                 # 4a
        return displayMessage("This project is not in your Shortlist.", "info")

    # Step 5: retrieve the IDP details
    # an empty dict means the IDP no longer exists
    idp = controller.getIDPDetails(idpID)
    if not idp:                                                         # 5a
        return displayMessage("This project is no longer available.", "err")

    # Steps 6-7: display them, with a link back to the Shortlist
    return displayIDPDetails(idp)

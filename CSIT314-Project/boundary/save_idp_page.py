"""«Boundary» SaveIDPPage — #34 Save IDP to Shortlist
(no class: the "Save to Favourite List" button on idp_details.html + route function).
The idpID comes from the URL (<int:idpID>), so there is no typed input to validate."""
from flask import Blueprint, session, flash

from control import SaveIDPController
from boundary.view_idp_page import displayIDPDetails, displayError

save_favourite = Blueprint("save_favourite", __name__)


def displayResult(idp: dict, message: str, category: str) -> str:      # step 5 / 3a / 4a
    if not idp:                                  # the IDP is gone: one error message only
        return displayError(message)
    flash(message, category)
    # The details page is shown again here (not redirected to), so saving does not add a view (#40)
    return displayIDPDetails(idp)


@save_favourite.route("/idp/<int:idpID>/save", methods=["POST"])
def saveRoute(idpID: int) -> str:
    # Steps 1-2: Customer is viewing the IDP and selects "Save to Favourite List"
    customerU = session["u"]
    controller = SaveIDPController()

    # Step 3: already saved?
    alreadySaved = controller.isIDPSaved(customerU, idpID)
    if alreadySaved:                                                    # 3a
        return displayResult(controller.getIDPDetails(idpID),
                             "This IDP is already in your favourite list.", "info")

    # Step 4: save it
    saved = controller.saveIDP(customerU, idpID)
    if not saved:                                                       # 4a
        return displayResult(controller.getIDPDetails(idpID),
                             "This IDP could not be saved. Please try again.", "err")

    # Step 5: confirm
    return displayResult(controller.getIDPDetails(idpID), "IDP saved to your favourite list.", "ok")

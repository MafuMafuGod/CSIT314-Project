"""«Boundary» DeletePortfolioPage — #55 Delete current project / #60 Delete past project
(no class: the Delete pop-up in portfolio.html / portfolio_view.html + route function).
Step 2 (confirmation) and 3a (Cancel closes it, nothing is deleted) happen in the pop-up."""
from flask import Blueprint, session, flash, redirect, url_for

from control import DeleteCurrentProjectController, DeletePastProjectController

delete_portfolio = Blueprint("delete_portfolio", __name__)

CONTROLLERS = {"current": DeleteCurrentProjectController, "past": DeletePastProjectController}


def displayResult(kind: str, message: str, category: str) -> str:      # step 5 / 4a
    flash(message, category)
    return redirect(url_for("portfolio.portfolioPage", kind=kind))


@delete_portfolio.route("/designer/portfolio/<any(current, past):kind>/<int:idpID>/delete", methods=["POST"])
def deleteProjectRoute(kind: str, idpID: int) -> str:
    # Steps 1-3: ID clicked Delete and confirmed in the pop-up
    # Step 4: remove the project from the portfolio
    deleted = CONTROLLERS[kind]().deleteProject(session["u"], idpID)
    if not deleted:                                                     # 4a
        return displayResult(kind, "The project could not be deleted. Please try again.", "err")
    return displayResult(kind, "The project was deleted from your portfolio.", "ok")

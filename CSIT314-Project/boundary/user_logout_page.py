"""«Boundary» UserLogoutPage — #07 User Logout, #15 Interior Designer Logout, #37 Customer Logout
(no class: base.html Log Out button, logged_out.html + route functions)."""
from flask import Blueprint, render_template

from control import UserLogoutController

logout = Blueprint("logout", __name__)


def displayLogoutSuccess() -> str:                                       # step 3
    return render_template("logged_out.html")

# POST only: the Log out button in the navbar sends a form,
# so typing /logout in the address bar does nothing
@logout.route("/logout", methods=["POST"])
def logoutRoute() -> str:
    # Step 1: user clicks Log Out
    # Steps 2-5: terminate the active session (returns logoutSuccess)
    # ask the Control to end the session
    UserLogoutController().userAccountLogout()
    # Step 6: display the logged-out confirmation page
    return displayLogoutSuccess()

"""«Boundary» UserLoginPage — #06 User Login, #14 Interior Designer Login, #31 Customer Login,
#70 Platform Admin Login
(no class: login.html + route functions). One login page for every profile."""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from control import UserLoginController
from boundary.profiles import getProfileLabels

login = Blueprint("login", __name__)


def displayLoginForm(error: str = None, u: str = "", missingFields: list = None) -> str:
    # Password is never sent back to the page, so the field is always cleared.
    return render_template("login.html", error=error, u=u,
                           missingFields=missingFields or [])


def validateFields(u: str, p: str) -> list:                              # step 4
    """Boundary input check: all required fields filled.
    Returns missingFields, e.g. ["u", "p"]; empty list = all filled."""
    missingFields = []
    if not u:
        missingFields.append("u")
    if not p:
        missingFields.append("p")
    return missingFields


def displayFieldWarning(u: str, missingFields: list) -> str:            # 3b
    return displayLoginForm(None, u, missingFields)


def displayLoginError(u: str) -> str:                                    # 3a
    return displayLoginForm("Invalid username or password", u)


def displayLoginSuccess(profile: str) -> str:                               # step 6
    flash(f"Logged in successfully as {getProfileLabels().get(profile, profile)}.", "ok")
    return redirect(url_for("home.displayHome"))


def submitLogin(u: str, p: str) -> str:
    # Steps 2-3: user entered credentials and clicked "Log In"

    # Step 4: Boundary checks required fields itself
    missingFields = validateFields(u, p)
    if missingFields:
        return displayFieldWarning(u, missingFields)

    # Step 5: verify credentials
    controller = UserLoginController()
    loginSuccess = controller.userAccountLogin(u, p)
    if not loginSuccess:
        return displayLoginError(u)

    # Step 6: check profile for access permissions
    profile = controller.getUserProfile(u)
    session["u"] = u
    session["profile"] = profile
    return displayLoginSuccess(profile)


@login.route("/", methods=["GET"])
@login.route("/login", methods=["GET", "POST"])
def loginPage() -> str:
    # Step 1: user arrives at login page
    if request.method == "GET":
        return displayLoginForm()
    return submitLogin(request.form.get("u", "").strip(), request.form.get("p", ""))

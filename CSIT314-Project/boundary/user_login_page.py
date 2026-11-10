"""«Boundary» UserLoginPage — #06 User Login, #14 Interior Designer Login, #31 Customer Login,
#70 Platform Admin Login
(no class: login.html + route functions). One login page for every profile."""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from control import UserLoginController
from boundary.profiles import getProfileLabels

# Blueprint = group of routes (web addresses). app.py registers this one
login = Blueprint("login", __name__)

# error = message to show, u = email to refill, missingFields = boxes to warn about
def displayLoginForm(error: str = None, u: str = "", missingFields: list = None) -> str:
    # Password is never sent back to the page, so the field is always cleared.
    return render_template("login.html", error=error, u=u,
                           missingFields=missingFields or [])


# Returns the names of the empty fields, e.g. ["u"]. An empty list means all filled
def validateFields(u: str, p: str) -> list:                              # step 4
    """Boundary input check: all required fields filled.
    Returns missingFields, e.g. ["u", "p"]; empty list = all filled."""
    missingFields = []   # start with an empty list and add a name for each empty box
    if not u:            # email left empty
        missingFields.append("u")
    if not p:            # password left empty
        missingFields.append("p")
    return missingFields

# Shows the form again with a warning under each empty box (alternate flow #31 5a)
def displayFieldWarning(u: str, missingFields: list) -> str:            
    return displayLoginForm(None, u, missingFields)

# Shows the form again with a red error banner (alternate flow #31 6a)
def displayLoginError(u: str) -> str:                                    
    return displayLoginForm("Invalid username or password", u)

# Login worked: show a green message and the home page
def displayLoginSuccess(profile: str) -> str:            
    # flash() stores a short message that the next page shows once       # step 6
    flash(f"Logged in successfully as {getProfileLabels().get(profile, profile)}.", "ok")
    return redirect(url_for("home.displayHome"))

# Runs the login steps in order: check fields, check password, save the user in the session
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
    # session = the browser's login memory. Saving u and profile means "this user is logged in"
    session["u"] = u
    session["profile"] = profile
    return displayLoginSuccess(profile)


@login.route("/", methods=["GET"])
@login.route("/login", methods=["GET", "POST"])
def loginPage() -> str:
    # Step 1: user arrives at login page
    # GET: show an empty login form
    if request.method == "GET":
        return displayLoginForm()
    # POST: the user clicked Log in
    return submitLogin(request.form.get("u", "").strip(), request.form.get("p", ""))

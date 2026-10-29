"""
4RENO - Use Case #06: User Login
       Use Case #07: User Logout
       Use Case #42: Create User Account
       Use Case #43: View User Account

BCE structure
  «Boundary»  UserLoginPage        -> no class 
  «Control»   UserLoginController  -> class
  «Entity»    UserAccount          -> class

Run:  python app.py   
Demo accounts (u / p / role):
  homeowner@4reno.com / password123 / homeowner
  designer@4reno.com  / design123   / designer
  admin@4reno.com     / admin123    / admin
"""
import secrets
from typing import Optional
from flask import (Flask, Blueprint, render_template, render_template_string,
                   request, session, abort, flash, redirect, url_for)

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

# ======================================================================
# «Entity» UserAccount
# ======================================================================
class UserAccount:
    """A registered user account. Owns the account data and checks credentials."""

    _accounts = []                      # stand-in for the database table

    def __init__(self, name: str, u: str, p: str, role: str, status: str = "active") -> None:
        self._name = name                # full name
        self._u = u                      # username (email)
        self._p = p                      # password
        self._role = role                # homeowner / designer / admin
        self._status = status            # active / suspended

    # ---- private helper ----------------------------------------------
    @classmethod
    def _findAccount(cls, u: str) -> Optional["UserAccount"]:
        for account in cls._accounts:
            if account._u == u:
                return account
        return None

    # ---- public methods (called by the Controller) ----------------------
    @classmethod
    def userAccountLogin(cls, u: str, p: str) -> bool:
        """Step 5: verify credentials against the database."""
        account = cls._findAccount(u)
        return account is not None and account._p == p

    @classmethod
    def getRole(cls, u: str) -> str:
        """Step 6: return the user's assigned role."""
        account = cls._findAccount(u)
        return account._role if account else ""

    # ---- used by Create User Account (#42) ----------------------------
    @classmethod
    def accountExists(cls, u: str) -> bool:
        """step 6b"""
        return cls._findAccount(u) is not None

    @classmethod
    def createAccount(cls, name: str, u: str, p: str, role: str) -> bool:
        """step 7"""
        cls._accounts.append(UserAccount(name, u, p, role))
        return True

    # ---- used by View User Account (#43) ------------------------------
    def _toDict(self) -> dict:
        """Account details for display (password is never included)."""
        return {"name": self._name, "u": self._u, "role": self._role, "status": self._status}

    @classmethod
    def getAllAccounts(cls) -> list:
        """#43 step 1: return every account, for the User Management list."""
        return [account._toDict() for account in cls._accounts]

    @classmethod
    def selectUserAccount(cls, u: str) -> dict:
        """#43 step 3: return one account's details ({} if not found)."""
        account = cls._findAccount(u)
        return account._toDict() if account else {}


# Sample data
UserAccount._accounts = [
    UserAccount("Hannah Tan", "homeowner@4reno.com", "password123", "homeowner"),
    UserAccount("Daniel Lim", "designer@4reno.com", "design123", "designer"),
    UserAccount("Alex Wong", "admin@4reno.com", "admin123", "admin"),
]


# ======================================================================
# «Control» UserLoginController
# ======================================================================
class UserLoginController:
    """Receives requests from the Boundary and applies them to the Entity."""

    def validateFields(self, u: str, p: str) -> list:
        """Step 4: check all required fields are filled.
        Returns missingFields, e.g. ["u", "p"]; empty list = all filled."""
        missingFields = []
        if not u:
            missingFields.append("u")
        if not p:
            missingFields.append("p")
        return missingFields

    def userAccountLogin(self, u: str, p: str) -> bool:
        """Step 5: returns loginSuccess (True / False) from the Entity."""
        return UserAccount.userAccountLogin(u, p)

    def getUserRole(self, u: str) -> str:
        """Step 6: returns role from the Entity."""
        return UserAccount.getRole(u)



# «Boundary» UserLoginPage  (no class: templates + route functions)

login = Blueprint("login", __name__)


def displayLoginForm(error: str = None, u: str = "", missingFields: list = None) -> str:
    # Password is never sent back to the page, so the field is always cleared.
    return render_template("login.html", error=error, u=u,
                           missingFields=missingFields or [])


def displayFieldWarning(u: str, missingFields: list) -> str:            # 3b
    return displayLoginForm(None, u, missingFields)


def displayLoginError(u: str) -> str:                                    # 3a
    return displayLoginForm("Invalid username or password", u)


def displayLoginSuccess(u: str, role: str) -> str:                       # step 6
    flash(f"Logged in successfully as {role.capitalize()}.", "ok")
    return render_template("home.html", categories=[], featured=[])


def submitLogin(u: str, p: str) -> str:
    # Steps 2-3: user entered credentials and clicked "Log In"
    controller = UserLoginController()

    # Step 4: check required fields
    missingFields = controller.validateFields(u, p)
    if missingFields:
        return displayFieldWarning(u, missingFields)

    # Step 5: verify credentials
    loginSuccess = controller.userAccountLogin(u, p)
    if not loginSuccess:
        return displayLoginError(u)

    # Step 6: check role for access permissions
    role = controller.getUserRole(u)
    session["u"] = u
    session["role"] = role
    return displayLoginSuccess(u, role)


@login.route("/", methods=["GET"])
@login.route("/login", methods=["GET", "POST"])
def loginPage() -> str:
    # Step 1: user arrives at login page
    if request.method == "GET":
        return displayLoginForm()
    # Form submitted: pass the entered u and p to submitLogin
    return submitLogin(request.form.get("u", "").strip(), request.form.get("p", ""))



#                          USE CASE #07 : USER LOGOUT


class UserSession:
    """The logged-in user's active session (the u and role saved at login)."""

    def __init__(self) -> None:
        self._u = session.get("u", "")
        self._role = session.get("role", "")

    def killSession(self) -> bool:
        """Step 2: terminate the active session.
        Returns logoutSuccess: True if a session was ended, False if none was active."""
        if not self._u:
            return False
        session.clear()
        self._u = ""
        self._role = ""
        return True


# ======================================================================
# «Control» UserLogoutController
# ======================================================================
class UserLogoutController:
    """Receives the logout request from the Boundary and applies it to the Entity."""

    def userAccountLogout(self) -> bool:
        """Returns logoutSuccess from the Entity."""
        return UserSession().killSession()


# ======================================================================
# «Boundary» UserLogoutPage  (no class: base.html Log Out button,
#                             logged_out.html + route functions)
# ======================================================================
logout = Blueprint("logout", __name__)


def displayLogoutSuccess() -> str:                                       # step 3
    return render_template("logged_out.html")


def displayNotLoggedIn() -> str:                                         # 1a
    return render_template("login.html", error=None, u="", missingFields=[])


@logout.route("/logout", methods=["POST"])
def logoutRoute() -> str:
    # Step 1: user clicks Log Out
    logoutSuccess = UserLogoutController().userAccountLogout()

    if logoutSuccess:
        return displayLogoutSuccess()       # [logoutSuccess = true]
    return displayNotLoggedIn()             # [else]


#                 USE CASE #42 : CREATE USER ACCOUNT

# «Control» CreateUserAccountController
class CreateUserAccountController:
    """Validates new account data and creates the account."""

    _VALID_ROLES = ["homeowner", "designer", "admin"]

    def validateAccountData(self, name: str, u: str, p: str, role: str) -> dict:
        """Step 6: validate entered data.
        Returns fieldErrors, e.g. {"u": "..."}; empty dict = all valid."""
        fieldErrors = {}
        if not name:
            fieldErrors["name"] = "Please enter the user's name."
        if not u:
            fieldErrors["u"] = "Please enter an email address."
        elif "@" not in u or "." not in u.split("@")[-1]:
            fieldErrors["u"] = "Please enter a valid email address."
        elif UserAccount.accountExists(u):                                      # 6b
            fieldErrors["u"] = "An account with this email already exists. Please use a different email."
        if not p:
            fieldErrors["p"] = "Please enter an initial password."
        if role not in CreateUserAccountController._VALID_ROLES:
            fieldErrors["role"] = "Please select a role."
        return fieldErrors

    def createUserAccount(self, name: str, u: str, p: str, role: str) -> bool:
        """Step 7: returns accountCreated from the Entity."""
        return UserAccount.createAccount(name, u, p, role)



# «Boundary» CreateUserAccountPage  
# Precondition (User Admin logged in) is enforced by requireAdmin() further below.

create_account = Blueprint("create_account", __name__)


def displayCreateAccountForm(fieldErrors: dict = None, successMessage: str = None) -> str:
    return render_template("create_account.html", fieldErrors=fieldErrors or {},
                           successMessage=successMessage, active="users")


def displayValidationErrors(fieldErrors: dict) -> str:                          # 6a / 6b
    return displayCreateAccountForm(fieldErrors=fieldErrors)


def displayCreateAccountSuccess(u: str) -> str:                                  # step 8
    return displayCreateAccountForm(successMessage=f"User account for {u} was created successfully.")


def submitCreateAccount(name: str, u: str, p: str, role: str) -> str:
    # Steps 4-5: admin entered details and submitted
    controller = CreateUserAccountController()

    # Step 6: validate (includes 6b: email already exists)
    fieldErrors = controller.validateAccountData(name, u, p, role)
    if fieldErrors:
        return displayValidationErrors(fieldErrors)

    # Steps 7-8: create the account and confirm
    controller.createUserAccount(name, u, p, role)
    return displayCreateAccountSuccess(u)


@create_account.route("/admin/users/create", methods=["GET", "POST"])
def createAccountPage() -> str:
    # Steps 2-3: admin clicks "Create New User", system shows the form
    if request.method == "GET":
        return displayCreateAccountForm()
    # Form submitted: pass the entered details to submitCreateAccount
    return submitCreateAccount(request.form.get("name", "").strip(),
                               request.form.get("u", "").strip(),
                               request.form.get("p", ""),
                               request.form.get("role", ""))



#                  USE CASE #43 : VIEW USER ACCOUNT


# «Control» ViewUserAccountController

class ViewUserAccountController:
    """Gets the account list and a selected account's details from the Entity."""

    def getUserAccountList(self) -> list:
        """Step 1: returns userAccounts."""
        return UserAccount.getAllAccounts()

    def selectUserAccount(self, u: str) -> dict:
        """Steps 2-3: returns userAccount."""
        return UserAccount.selectUserAccount(u)



# «Boundary» ViewUserAccountPage  (no class: user_management.html,
#                                  view_account.html + route functions)
# Precondition (User Admin logged in) is enforced by requireAdmin() further below.

user_management = Blueprint("user_management", __name__)


def displayUserAccountList(userAccounts: list) -> str:                          # step 1
    return render_template("user_management.html", userAccounts=userAccounts, active="users")


def displayUserAccountDetails(userAccount: dict) -> str:                        # step 3
    return render_template("view_account.html", userAccount=userAccount, active="users")


@user_management.route("/admin/users")
def userManagementPage() -> str:
    # Step 1: User Admin opens the User Management section
    userAccounts = ViewUserAccountController().getUserAccountList()
    return displayUserAccountList(userAccounts)


@user_management.route("/admin/users/view/<u>")
def viewUserAccount(u: str) -> str:
    # Step 2: User Admin selects a user account from the list
    userAccount = ViewUserAccountController().selectUserAccount(u)
    if not userAccount:              # precondition: account must exist
        abort(404)
    # Step 3: display its details
    return displayUserAccountDetails(userAccount)



# Placeholder pages (NOT part of use cases #06 / #07 / #42 / #43)
# These only exist so the navbar links in base.html work. Each one gets
# replaced with real Boundary / Control / Entity code in its own use case.


COMING_SOON = """{% extends "base.html" %}
{% block title %}{{ name }} | 4RENO{% endblock %}
{% block content %}<h1>{{ name }}</h1><div class="banner info">Coming soon.</div>{% endblock %}"""

home = Blueprint("home", __name__)
search_idp = Blueprint("search_idp", __name__)
search_shortlist = Blueprint("search_shortlist", __name__)


@home.route("/home")
def displayHome():
    return render_template("home.html", categories=[], featured=[])


@search_idp.route("/search")
def searchPage():
    return render_template_string(COMING_SOON, name="Interior Designers", active="search")


@search_shortlist.route("/shortlist")
def shortlistPage():
    return render_template_string(COMING_SOON, name="My Shortlist", active="shortlist")



# Infrastructure (not part of the BCE diagrams): admin guard + CSRF protection

@app.context_processor
def inject_csrf():
    def csrf_token():
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(16)
        return session["csrf"]
    return {"csrf_token": csrf_token}


@app.before_request
def requireAdmin():
    """Precondition for #42: only a logged-in User Admin may open /admin pages."""
    if request.path.startswith("/admin") and session.get("role") != "admin":
        flash("You do not have permission to access User Management.", "err")
        return redirect(url_for("home.displayHome"))


@app.before_request
def check_csrf():
    if request.method == "POST" and request.form.get("csrf_token") != session.get("csrf"):
        abort(400, "Invalid CSRF token")


for bp in (login, logout, create_account, home, search_idp, search_shortlist,
           user_management):
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)

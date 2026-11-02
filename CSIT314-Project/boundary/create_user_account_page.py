"""«Boundary» CreateUserAccountPage — #42 Create User Account
(no class: create_account.html + route functions)."""
from flask import Blueprint, render_template, request

from control import CreateUserAccountController

create_account = Blueprint("create_account", __name__)

VALID_PROFILES = ["homeowner", "designer", "admin"]


def displayCreateAccountForm(fieldErrors: dict = None, successMessage: str = None) -> str:
    return render_template("create_account.html", fieldErrors=fieldErrors or {},
                           successMessage=successMessage, active="users")


def validateAccountData(name: str, u: str, p: str, profile: str) -> dict:   # step 6
    """Boundary input check: fields filled and in the right format.
    Returns fieldErrors, e.g. {"u": "..."}; empty dict = all valid."""
    fieldErrors = {}
    if not name:
        fieldErrors["name"] = "Please enter the user's name."
    if not u:
        fieldErrors["u"] = "Please enter an email address."
    elif "@" not in u or "." not in u.split("@")[-1]:
        fieldErrors["u"] = "Please enter a valid email address."
    if not p:
        fieldErrors["p"] = "Please enter an initial password."
    if profile not in VALID_PROFILES:
        fieldErrors["profile"] = "Please select a profile."
    return fieldErrors


def displayValidationErrors(fieldErrors: dict) -> str:                   # 6a / 6b
    return displayCreateAccountForm(fieldErrors=fieldErrors)


def displayCreateAccountSuccess(u: str) -> str:                          # step 8
    return displayCreateAccountForm(successMessage=f"User account for {u} was created successfully.")


def submitCreateAccount(name: str, u: str, p: str, profile: str) -> str:
    # Steps 4-5: admin entered details and submitted

    # Step 6 (6a): Boundary validates the input itself
    fieldErrors = validateAccountData(name, u, p, profile)
    if fieldErrors:
        return displayValidationErrors(fieldErrors)

    # Step 6b: email already registered? (needs stored data -> via Control)
    controller = CreateUserAccountController()
    accountExists = controller.checkAccountExists(u)
    if accountExists:
        return displayValidationErrors(
            {"u": "An account with this email already exists. Please use a different email."})

    # Steps 7-8: create the account and confirm
    controller.createUserAccount(name, u, p, profile)
    return displayCreateAccountSuccess(u)


@create_account.route("/admin/users/create", methods=["GET", "POST"])
def createAccountPage() -> str:
    # Steps 2-3: admin clicks "Create New User", system shows the form
    if request.method == "GET":
        return displayCreateAccountForm()
    return submitCreateAccount(request.form.get("name", "").strip(),
                               request.form.get("u", "").strip(),
                               request.form.get("p", ""),
                               request.form.get("profile", ""))

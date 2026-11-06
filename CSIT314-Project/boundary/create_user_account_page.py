"""«Boundary» CreateUserAccountPage — #42 Create User Account
(no class: create_account.html + route functions)."""
from flask import Blueprint, render_template, request

from control import CreateUserAccountController
from boundary.profiles import getAccountFormOptions, validateAccountDetails

create_account = Blueprint("create_account", __name__)


def displayCreateAccountForm(options: dict, fieldErrors: dict = None,
                             successMessage: str = None) -> str:
    return render_template("create_account.html", fieldErrors=fieldErrors or {},
                           successMessage=successMessage, active="users", **options)


def validateAccountData(name: str, u: str, p: str, profile: str, permissions: list,
                        options: dict) -> dict:                          # step 6 (6a)
    """Boundary input check: fields filled, in the right format, and choices from the lists.
    Returns fieldErrors, e.g. {"u": "..."}; empty dict = all valid."""
    fieldErrors = validateAccountDetails(name, u, profile, permissions,
                                         options["profileOptions"], options["permissionGroups"])
    if not p:
        fieldErrors["p"] = "Please enter an initial password."
    return fieldErrors


def displayValidationErrors(options: dict, fieldErrors: dict) -> str:   # 6a / 6b
    return displayCreateAccountForm(options, fieldErrors=fieldErrors)


def displayCreateAccountSuccess(options: dict, u: str) -> str:          # step 8
    return displayCreateAccountForm(options, successMessage=f"User account for {u} was created successfully.")


def submitCreateAccount(name: str, u: str, p: str, profile: str, permissions: list) -> str:
    # Steps 4-5: admin entered details and submitted
    options = getAccountFormOptions()

    # Step 6 (6a): Boundary validates the input itself
    fieldErrors = validateAccountData(name, u, p, profile, permissions, options)
    if fieldErrors:
        return displayValidationErrors(options, fieldErrors)

    # Step 6b: email already registered? (needs stored data -> via Control)
    controller = CreateUserAccountController()
    accountExists = controller.checkAccountExists(u)
    if accountExists:
        return displayValidationErrors(
            options, {"u": "An account with this email already exists. Please use a different email."})

    # Steps 7-8: create the account and confirm
    controller.createUserAccount(name, u, p, profile, permissions)
    return displayCreateAccountSuccess(options, u)


@create_account.route("/admin/users/create", methods=["GET", "POST"])
def createAccountPage() -> str:
    # Steps 2-3: admin clicks "Create user", system shows the form
    if request.method == "GET":
        return displayCreateAccountForm(getAccountFormOptions())
    return submitCreateAccount(request.form.get("name", "").strip(),
                               request.form.get("u", "").strip(),
                               request.form.get("p", ""),
                               request.form.get("profile", ""),
                               request.form.getlist("permissions"))

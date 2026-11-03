"""«Boundary» ViewUserAccountPage — #43 View User Account
(no class: user_management.html, view_account.html + route functions)."""
from flask import Blueprint, render_template, abort

from control import ViewUserAccountController

user_management = Blueprint("user_management", __name__)


def displayUserAccountList(userAccounts: list) -> str:                  # step 1
    return render_template("user_management.html", userAccounts=userAccounts, active="users")


def displayUserAccountDetails(userAccount: dict) -> str:                # step 3
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

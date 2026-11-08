"""«Boundary» ViewUserAccountPage — #43 View User Account and #46 Search User Account
(no class: user_management.html, view_account.html + route functions).
The list and the search share one page: no search words = the full list (#43)."""
from flask import Blueprint, render_template, request, abort, flash

from control import ViewUserAccountController, SearchUserAccountController
from boundary.profiles import getProfileLabels, STATUSES, MAX_SEARCH_LENGTH

user_management = Blueprint("user_management", __name__)


def displayUserAccountList(userAccounts: list) -> str:                  # #43 step 1 / #46 step 6
    # An empty list after a search shows "No user accounts found" (#46 7a) in the template
    return render_template("user_management.html", userAccounts=userAccounts, active="users")


def displayUserAccountDetails(userAccount: dict) -> str:                # #43 step 3
    return render_template("view_account.html", userAccount=userAccount, active="users")


def validateSearchCriteria(q: str, status: str, profile: str) -> str:  # #46 step 4
    """Boundary input check. Returns an error message, "" = valid."""
    if len(q) > MAX_SEARCH_LENGTH:
        return f"Search words must be {MAX_SEARCH_LENGTH} characters or fewer."
    if status and status not in STATUSES:
        return "Please choose a status from the list."
    if profile and profile not in getProfileLabels():
        return "Please choose a profile from the list."
    return ""


def displaySearchError(error: str) -> str:                              # #46 step 4 (invalid)
    flash(error, "err")
    return displayUserAccountList([])


def submitSearch(q: str, status: str, profile: str) -> str:
    # #46 step 4: Boundary validates the search criteria
    error = validateSearchCriteria(q, status, profile)
    if error:
        return displaySearchError(error)
    # Step 5: search for matching accounts
    userAccounts = SearchUserAccountController().searchUserAccounts(q, status, profile)
    # Step 6: display them (7a: empty list -> "No user accounts found")
    return displayUserAccountList(userAccounts)


@user_management.route("/admin/users")
def userManagementPage() -> str:
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    profile = request.args.get("profile", "").strip()
    if q or status or profile:
        # #46 steps 2-3: User Admin entered search criteria and submitted
        return submitSearch(q, status, profile)
    # #43 step 1: User Admin opens the User Management section
    userAccounts = ViewUserAccountController().getUserAccountList()
    return displayUserAccountList(userAccounts)


@user_management.route("/admin/users/view/<u>")
def viewUserAccount(u: str) -> str:
    # #43 step 2: User Admin selects a user account from the list
    userAccount = ViewUserAccountController().selectUserAccount(u)
    if not userAccount:              # precondition: account must exist
        abort(404)
    # Step 3: display its details
    return displayUserAccountDetails(userAccount)

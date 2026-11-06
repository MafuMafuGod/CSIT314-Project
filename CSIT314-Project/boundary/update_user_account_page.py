"""«Boundary» UpdateUserAccountPage — #44 Update User Account
(no class: edit_account.html + route functions)."""
from flask import Blueprint, render_template, request, session, abort

from control import UpdateUserAccountController
from boundary.profiles import (getAccountFormOptions, getProfileLabels, validateAccountDetails,
                               describePermissionChanges)

update_account = Blueprint("update_account", __name__)


def getProfileChoices(currentProfile: str) -> dict:
    """Active profiles, plus the account's current one even if it has been suspended."""
    choices = dict(getAccountFormOptions()["profileOptions"])
    if currentProfile not in choices:
        choices[currentProfile] = getProfileLabels().get(currentProfile, currentProfile)
    return choices


def displayUpdateForm(accountU: str, userAccount: dict, fieldErrors: dict = None) -> str:   # step 2
    return render_template("edit_account.html", accountU=accountU, userAccount=userAccount,
                           selectedPermissions=userAccount["permissions"],
                           permissionGroups=getAccountFormOptions()["permissionGroups"],
                           profileOptions=getProfileChoices(userAccount["profile"]),
                           fieldErrors=fieldErrors or {}, saved=False, active="users")


def validateUpdatedData(name: str, u: str, profile: str, permissions: list,
                        profileChoices: dict) -> dict:                   # step 3 (5a)
    """Boundary input check. Returns fieldErrors; empty dict = all valid."""
    return validateAccountDetails(name, u, profile, permissions, profileChoices,
                                  getAccountFormOptions()["permissionGroups"])


def listChanges(before: dict, after: dict) -> list:
    """The "What changed" summary: (label, text) for each field that changed."""
    labels = getProfileLabels()
    changes = []
    if before["name"] != after["name"]:
        changes.append(("Full name", f"{before['name']} → {after['name']}"))
    if before["u"] != after["u"]:
        changes.append(("Email", f"{before['u']} → {after['u']}"))
    if before["profile"] != after["profile"]:
        changes.append(("Profile", f"{labels.get(before['profile'], before['profile'])} → "
                                   f"{labels.get(after['profile'], after['profile'])}"))
    permissionChanges = describePermissionChanges(before["permissions"], after["permissions"])
    if permissionChanges:
        changes.append(("Permissions", permissionChanges))
    return changes


def displayValidationErrors(accountU: str, typed: dict, fieldErrors: dict) -> str:   # 5a
    return displayUpdateForm(accountU, typed, fieldErrors)


def displayUpdateSuccess(newU: str, changes: list) -> str:              # step 5
    return render_template("edit_account.html", accountU=newU, saved=True, changes=changes,
                           active="users")


def submitUpdate(accountU: str, before: dict, name: str, u: str, profile: str,
                 permissions: list) -> str:
    typed = {"name": name, "u": u, "profile": profile, "permissions": permissions}

    # Step 3: Boundary validates the updated information
    fieldErrors = validateUpdatedData(name, u, profile, permissions,
                                      getProfileChoices(before["profile"]))
    if fieldErrors:
        return displayValidationErrors(accountU, typed, fieldErrors)

    # Step 3: a changed email must not belong to another account (stored data -> via Control)
    controller = UpdateUserAccountController()
    if u.lower() != accountU.lower():
        accountExists = controller.checkAccountExists(u)
        if accountExists:
            return displayValidationErrors(accountU, typed, {
                "u": "An account with this email already exists. Please use a different email."})

    # Step 4: save the updated details
    controller.updateUserAccount(accountU, name, u, profile, permissions)

    # The admin edited their own account: keep their session in step with it
    if session.get("u", "").lower() == accountU.lower():
        session["u"] = u
        session["profile"] = profile

    # Step 5: success message with what changed
    return displayUpdateSuccess(u, listChanges(before, typed))


@update_account.route("/admin/users/edit/<u>", methods=["GET", "POST"])
def updateAccountPage(u: str) -> str:
    # Step 1: User Admin opens the account from User Management and clicks Edit
    before = UpdateUserAccountController().selectUserAccount(u)
    if not before:                       # precondition: the account exists
        abort(404)
    if request.method == "GET":
        return displayUpdateForm(before["u"], before)
    # Step 2: User Admin edited the details and clicked Save
    return submitUpdate(before["u"], before,
                        request.form.get("name", "").strip(),
                        request.form.get("u", "").strip(),
                        request.form.get("profile", ""),
                        request.form.getlist("permissions"))

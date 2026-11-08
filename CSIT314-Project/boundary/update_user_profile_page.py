"""«Boundary» UpdateUserProfilePage — #49 Update User Profile
(no class: edit_profile.html + route functions)."""
from flask import Blueprint, render_template, request, abort

from control import UpdateUserProfileController, ProfileOptionsController
from boundary.profiles import validateProfileDetails, describePermissionChanges

update_profile = Blueprint("update_profile", __name__)


def displayUpdateForm(profileName: str, userCount: int, form: dict, selectedPermissions: list,
                      fieldErrors: dict = None) -> str:                   # step 1
    return render_template("edit_profile.html", profileName=profileName, userCount=userCount,
                           form=form, selectedPermissions=selectedPermissions,
                           permissionGroups=ProfileOptionsController().getPermissionGroups(),
                           fieldErrors=fieldErrors or {}, saved=False, active="users")


def listChanges(before: dict, after: dict) -> list:
    """The "What changed" summary: (label, text) for each field that changed."""
    changes = []
    if before["name"] != after["name"]:
        changes.append(("Profile name", f"{before['name']} → {after['name']}"))
    if before["description"] != after["description"]:
        changes.append(("Description", after["description"] or "(removed)"))
    permissionChanges = describePermissionChanges(before["permissions"], after["permissions"])
    if permissionChanges:
        changes.append(("Permissions", permissionChanges))
    return changes


def displayUpdateSuccess(newName: str, changes: list) -> str:           # step 6
    return render_template("edit_profile.html", profileName=newName, saved=True,
                           changes=changes, active="users")


def submitUpdate(before: dict, userCount: int, name: str, description: str,
                 permissions: list) -> str:
    form = {"name": name, "description": description}

    # Step 4: Boundary validates the updated information and permissions
    fieldErrors = validateProfileDetails(name, description, permissions,
                                         ProfileOptionsController().getPermissionGroups())
    if fieldErrors:
        return displayUpdateForm(before["name"], userCount, form, permissions, fieldErrors)

    # Step 4: a new name must not belong to another profile (stored data -> via Control)
    controller = UpdateUserProfileController()
    if name.lower() != before["name"].lower() and controller.checkProfileExists(name):
        return displayUpdateForm(before["name"], userCount, form, permissions,
                                 {"name": "A profile with this name already exists."})

    # Step 5: save the changes
    updated = controller.updateUserProfile(before["name"], name, description, permissions)
    if not updated:                      # 8a: saving failed -> error, not success
        return displayUpdateForm(before["name"], userCount, form, permissions,
                                 {"name": "The profile could not be saved. Please try again."})

    # Step 6: success message with what changed
    return displayUpdateSuccess(name, listChanges(before, {"name": name, "description": description,
                                                          "permissions": permissions}))


@update_profile.route("/admin/profiles/edit/<name>", methods=["GET", "POST"])
def updateProfilePage(name: str) -> str:
    # Step 1: User Admin goes to the profile to update
    controller = UpdateUserProfileController()
    before = controller.selectUserProfile(name)
    if not before:                       # precondition: the profile exists
        abort(404)
    userCount = controller.getUserCount(before["key"])
    if request.method == "GET":
        return displayUpdateForm(before["name"], userCount,
                                 {"name": before["name"], "description": before["description"]},
                                 before["permissions"])
    # Steps 2-3: User Admin edited the details or permissions and submitted
    return submitUpdate(before, userCount,
                        request.form.get("name", "").strip(),
                        request.form.get("description", "").strip(),
                        request.form.getlist("permissions"))

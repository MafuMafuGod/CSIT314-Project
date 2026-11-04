"""«Boundary» CreateUserProfilePage — #47 Create User Profile
(no class: create_profile.html + route functions)."""
from flask import Blueprint, render_template, request

from control import CreateUserProfileController, ProfileOptionsController
from boundary.profiles import validateProfileDetails

create_profile = Blueprint("create_profile", __name__)


def displayCreateProfileForm(form: dict, selectedPermissions: list, startFrom: str = "",
                             fieldErrors: dict = None) -> str:            # step 4
    return render_template("create_profile.html", form=form, startFrom=startFrom,
                           selectedPermissions=selectedPermissions,
                           profileNames=CreateUserProfileController().getProfileNames(),
                           permissionGroups=ProfileOptionsController().getPermissionGroups(),
                           fieldErrors=fieldErrors or {}, createdProfile=None, active="users")


def displayValidationErrors(form: dict, permissions: list, fieldErrors: dict) -> str:   # 7a
    return displayCreateProfileForm(form, permissions, fieldErrors=fieldErrors)


def displayCreateProfileSuccess(createdProfile: dict) -> str:           # step 10
    return render_template("create_profile.html", createdProfile=createdProfile, active="users")


def submitCreateProfile(name: str, description: str, permissions: list) -> str:
    form = {"name": name, "description": description}

    # Step 8: Boundary validates the profile details
    fieldErrors = validateProfileDetails(name, description, permissions,
                                         ProfileOptionsController().getPermissionGroups())
    if fieldErrors:
        return displayValidationErrors(form, permissions, fieldErrors)

    # Step 8: the name must be unique (stored data -> via Control)
    controller = CreateUserProfileController()
    profileExists = controller.checkProfileExists(name)
    if profileExists:
        return displayValidationErrors(form, permissions,
                                       {"name": "A profile with this name already exists."})

    # Steps 9-10: create the profile with its permissions and confirm
    controller.createUserProfile(name, description, permissions)
    return displayCreateProfileSuccess({"name": name, "description": description,
                                        "permissions": permissions})


@create_profile.route("/admin/profiles/create", methods=["GET", "POST"])
def createProfilePage() -> str:
    if request.method == "GET":
        # Steps 3-4: User Admin clicks Create profile; "Start from" pre-ticks another
        # profile's permissions
        startFrom = request.args.get("start", "")
        return displayCreateProfileForm({"name": "", "description": ""},
                                        CreateUserProfileController().getStartingPermissions(startFrom),
                                        startFrom)
    # Steps 5-7: User Admin entered the details, ticked permissions and submitted
    return submitCreateProfile(request.form.get("name", "").strip(),
                               request.form.get("description", "").strip(),
                               request.form.getlist("permissions"))

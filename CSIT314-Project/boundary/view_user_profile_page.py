"""«Boundary» ViewUserProfilePage — #48 View User Profile and #51 Search User Profile
(no class: profile_management.html, view_profile.html + route functions).
The list and the search share one page: no search words = the full list (#48)."""
from flask import Blueprint, render_template, request, abort, flash

from control import ViewUserProfileController, SearchUserProfileController, ProfileOptionsController
from boundary.profiles import STATUSES, MAX_PROFILE_NAME_LENGTH

view_profile = Blueprint("view_profile", __name__)


def countPermissions(permissionGroups: dict) -> int:
    return sum(len(perms) for perms in permissionGroups.values())


def displayUserProfileList(userProfiles: list) -> str:                  # #48 step 2 / #51 step 5
    # Empty list: "No user profiles available" (#48 5a) or "No user profiles found" (#51 4a)
    controller = ViewUserProfileController()
    return render_template("profile_management.html", profiles=userProfiles,
                           totalProfiles=len(controller.getUserProfileList()),
                           totalPermissions=countPermissions(ProfileOptionsController().getPermissionGroups()),
                           active="users")


def displayUserProfileDetails(userProfile: dict, profileUsers: list) -> str:   # #48 step 5
    return render_template("view_profile.html", profile=userProfile, profileUsers=profileUsers,
                           permissionGroups=ProfileOptionsController().getPermissionGroups(),
                           active="users")


def validateSearchCriteria(q: str, status: str) -> str:                # #51 step 3
    """Boundary input check. Returns an error message, "" = valid."""
    if len(q) > MAX_PROFILE_NAME_LENGTH:
        return f"Search words must be {MAX_PROFILE_NAME_LENGTH} characters or fewer."
    if status and status not in STATUSES:
        return "Please choose a status from the list."
    return ""


def displaySearchError(error: str) -> str:                              # #51 step 3 (invalid)
    flash(error, "err")
    return displayUserProfileList([])


def submitSearch(q: str, status: str) -> str:
    # #51 step 3: Boundary validates the search criteria
    error = validateSearchCriteria(q, status)
    if error:
        return displaySearchError(error)
    # Step 4: search for matching profiles
    userProfiles = SearchUserProfileController().searchUserProfiles(q, status)
    # Step 5: display them (4a: empty list -> "No user profiles found")
    return displayUserProfileList(userProfiles)


@view_profile.route("/admin/profiles")
def profileManagementPage() -> str:
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    if q or status:
        # #51 steps 1-2: User Admin entered a name and/or status and clicked Search
        return submitSearch(q, status)
    # #48 steps 1-2: User Admin opens User Profile Management
    userProfiles = ViewUserProfileController().getUserProfileList()
    return displayUserProfileList(userProfiles)


@view_profile.route("/admin/profiles/view/<name>")
def viewUserProfile(name: str) -> str:
    # #48 step 3: User Admin selects the profile to view
    controller = ViewUserProfileController()
    userProfile = controller.selectUserProfile(name)
    if not userProfile:              # precondition: the profile exists
        abort(404)
    # Step 4: retrieve its users; step 5: display name, description and permissions
    return displayUserProfileDetails(userProfile, controller.getProfileUsers(userProfile["key"]))

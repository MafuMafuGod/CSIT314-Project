"""«Boundary» SuspendUserProfilePage — #50 Suspend User Profile
(no class: the Suspend pop-up in view_profile.html + route function)."""
from flask import Blueprint, request, session, flash, redirect, url_for

from control import SuspendUserProfileController, ViewUserProfileController
from boundary.profiles import validateReason

suspend_profile = Blueprint("suspend_profile", __name__)


def validateSuspension(profileKey: str, reason: str) -> str:            # step 2
    """Boundary input check. Returns an error message, "" = valid."""
    if profileKey == session.get("profile"):
        return "You cannot suspend your own profile."
    return validateReason(reason)


def displaySuspendResult(name: str, message: str, category: str) -> str:   # step 5 / error
    flash(message, category)
    return redirect(url_for("view_profile.viewUserProfile", name=name))


@suspend_profile.route("/admin/profiles/suspend/<name>", methods=["POST"])
def suspendProfileRoute(name: str) -> str:
    # Steps 1-2: User Admin selected the profile and clicked Suspend
    userProfile = ViewUserProfileController().selectUserProfile(name)
    reason = request.form.get("reason", "").strip()
    error = validateSuspension(userProfile.get("key", ""), reason)
    if error:
        return displaySuspendResult(name, error, "err")

    # Steps 3-4: set the status to Suspended; its users are blocked from signing in
    suspended = SuspendUserProfileController().suspendUserProfile(name, reason)
    if not suspended:                    # precondition failed: missing or already suspended
        return displaySuspendResult(name, "This profile could not be suspended. It may already be suspended.", "err")

    # Step 5: confirm
    return displaySuspendResult(name, "The profile has been suspended. Its users can no longer sign in.", "ok")

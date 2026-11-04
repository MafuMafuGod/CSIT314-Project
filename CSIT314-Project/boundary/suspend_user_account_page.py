"""«Boundary» SuspendUserAccountPage — #45 Suspend User Account
(no class: the Suspend pop-up in view_account.html + route function)."""
from flask import Blueprint, request, session, flash, redirect, url_for

from control import SuspendUserAccountController
from boundary.profiles import validateReason

suspend_account = Blueprint("suspend_account", __name__)


def validateSuspension(u: str, reason: str) -> str:                     # step 4
    """Boundary input check. Returns an error message, "" = valid."""
    if u.lower() == session.get("u", "").lower():
        return "You cannot suspend your own account."
    return validateReason(reason)


def displaySuspendResult(u: str, message: str, category: str) -> str:  # step 6 / error
    flash(message, category)
    return redirect(url_for("user_management.viewUserAccount", u=u))


@suspend_account.route("/admin/users/suspend/<u>", methods=["POST"])
def suspendAccountRoute(u: str) -> str:
    # Steps 2-4: User Admin chose the account, clicked Suspend and confirmed
    reason = request.form.get("reason", "").strip()
    error = validateSuspension(u, reason)
    if error:
        return displaySuspendResult(u, error, "err")

    # Step 5: set the status to Suspended (their session ends on their next page load)
    suspended = SuspendUserAccountController().suspendUserAccount(u, reason)
    if not suspended:                    # precondition failed: missing or already suspended
        return displaySuspendResult(u, "This account could not be suspended. It may already be suspended.", "err")

    # Step 6: confirm
    return displaySuspendResult(u, "The account has been suspended. The user can no longer sign in.", "ok")

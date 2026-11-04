"""Boundary helpers shared by the user account and user profile pages.
The profiles themselves are stored in the UserProfile entity; pages get them through the
ProfileOptionsController, so a profile created or renamed in #47 / #49 shows up everywhere."""
import re

from control import ProfileOptionsController

ACCOUNT_STATUSES = ["active", "suspended"]          # filter values for #46
PROFILE_STATUSES = ["active", "suspended"]          # filter values for #51
MAX_NAME_LENGTH = 100
MAX_SEARCH_LENGTH = 100
MAX_PROFILE_NAME_LENGTH = 60
MAX_DESCRIPTION_LENGTH = 200
MAX_REASON_LENGTH = 300


def getProfileLabels() -> dict:
    """{key: name} for every profile, e.g. {"designer": "Interior Designer"}."""
    return ProfileOptionsController().getProfileLabels()


def getAccountFormOptions() -> dict:
    """What the create / edit account forms need: profile choices, permission groups and
    each profile's default permissions."""
    controller = ProfileOptionsController()
    return {"profileOptions": controller.getActiveProfileOptions(),
            "permissionGroups": controller.getPermissionGroups(),
            "profileDefaults": controller.getProfileDefaults()}


def findInvalidPermissions(selected: list, permissionGroups: dict) -> list:
    """Boundary input check: ticked permissions that do not exist in the system."""
    allPermissions = {p for perms in permissionGroups.values() for p in perms}
    return [p for p in selected if p not in allPermissions]


def validateEmail(u: str) -> str:
    """Boundary input check shared by #42 and #44. Returns an error message, "" = valid."""
    if not u:
        return "Please enter an email address."
    if "@" not in u or "." not in u.split("@")[-1] or " " in u or len(u) > MAX_NAME_LENGTH:
        return "Please enter a valid email address."
    return ""


def validateReason(reason: str) -> str:
    """Boundary input check shared by #45 and #50."""
    if len(reason) > MAX_REASON_LENGTH:
        return f"Reason must be {MAX_REASON_LENGTH} characters or fewer."
    return ""


PROFILE_NAME_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9 &()'_-]*$"


def validateProfileDetails(name: str, description: str, permissions: list,
                           permissionGroups: dict) -> dict:
    """Boundary input check shared by #47 (step 8) and #49 (step 4).
    Returns fieldErrors; empty dict = all valid."""
    fieldErrors = {}
    if not name:
        fieldErrors["name"] = "Please enter a profile name."
    elif len(name) > MAX_PROFILE_NAME_LENGTH:
        fieldErrors["name"] = f"Profile name must be {MAX_PROFILE_NAME_LENGTH} characters or fewer."
    elif not re.match(PROFILE_NAME_PATTERN, name):
        fieldErrors["name"] = "Use letters, numbers, spaces and - _ & ( ) ' only."
    if len(description) > MAX_DESCRIPTION_LENGTH:
        fieldErrors["description"] = f"Description must be {MAX_DESCRIPTION_LENGTH} characters or fewer."
    if not permissions:
        fieldErrors["permissions"] = "Please select at least one permission."
    elif findInvalidPermissions(permissions, permissionGroups):
        fieldErrors["permissions"] = "Please choose permissions from the list."
    return fieldErrors

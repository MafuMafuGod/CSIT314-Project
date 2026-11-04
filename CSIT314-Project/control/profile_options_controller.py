"""«Control» ProfileOptionsController — shared profile and permission lookups.
Used by the pages that show or choose a profile: #42, #43, #44, #46, #47, #48, #49, and the
login message. Keeps the profile list in one place (the UserProfile entity)."""
from entity import UserProfile


class ProfileOptionsController:
    """Gets profile names, choices and permissions from the Entity."""

    def getProfileLabels(self) -> dict:
        """{key: name} for every profile."""
        return UserProfile.getProfileLabels()

    def getActiveProfileOptions(self) -> dict:
        """{key: name} for profiles that can be given to an account."""
        return UserProfile.getActiveProfileOptions()

    def getPermissionGroups(self) -> dict:
        """Every permission in the system, grouped."""
        return UserProfile.getPermissionGroups()

    def getProfileDefaults(self) -> dict:
        """{key: permissions} ticked when a profile is picked for an account."""
        return UserProfile.getProfileDefaults()

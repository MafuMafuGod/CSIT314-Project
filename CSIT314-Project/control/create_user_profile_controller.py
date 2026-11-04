"""«Control» CreateUserProfileController — #47 Create User Profile."""
from entity import UserProfile


class CreateUserProfileController:
    """Checks the profile name is unique and creates the profile."""

    def getProfileNames(self) -> list:
        """Step 4: existing profiles, for the "Start from" list."""
        return UserProfile.getProfileNames()

    def getStartingPermissions(self, name: str) -> list:
        """Step 6: the permissions of the profile picked in "Start from" ([] if none)."""
        return UserProfile.selectProfile(name).get("permissions", [])

    def checkProfileExists(self, name: str) -> bool:
        """Step 8: returns profileExists from the Entity."""
        return UserProfile.profileNameExists(name)

    def createUserProfile(self, name: str, description: str, permissions: list) -> bool:
        """Steps 9-10: returns created from the Entity."""
        return UserProfile.createProfile(name, description, permissions)

"""«Control» UpdateUserProfileController — #49 Update User Profile."""
from entity import UserAccount, UserProfile


class UpdateUserProfileController:
    """Gets the profile to edit, checks a new name is unique and saves the changes."""

    def selectUserProfile(self, name: str) -> dict:
        """Step 1: returns userProfile ({} = not found)."""
        return UserProfile.selectProfile(name)

    def getUserCount(self, profileKey: str) -> int:
        """Step 1: how many users the change affects."""
        return UserAccount.countAccountsByProfile().get(profileKey, 0)

    def checkProfileExists(self, name: str) -> bool:
        """Step 4: is the new name already used? Returns profileExists."""
        return UserProfile.profileNameExists(name)

    def updateUserProfile(self, name: str, newName: str, description: str, permissions: list) -> bool:
        """Step 5: returns updated (False = saving failed, 8a)."""
        return UserProfile.updateProfile(name, newName, description, permissions)

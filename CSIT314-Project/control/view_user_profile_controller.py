"""«Control» ViewUserProfileController — #48 View User Profile."""
from entity import UserAccount, UserProfile


def addUserCounts(profiles: list) -> list:
    """Adds userCount to each profile (shared with #51 search)."""
    counts = UserAccount.countAccountsByProfile()
    for profile in profiles:
        profile["userCount"] = counts.get(profile["key"], 0)
    return profiles


class ViewUserProfileController:
    """Gets the profile list, one profile's details and its users from the Entities."""

    def getUserProfileList(self) -> list:
        """Step 2: returns userProfiles with user counts ([] = none exist, 5a)."""
        return addUserCounts(UserProfile.getAllProfiles())

    def selectUserProfile(self, name: str) -> dict:
        """Step 4: returns userProfile ({} = not found)."""
        return UserProfile.selectProfile(name)

    def getProfileUsers(self, profileKey: str) -> list:
        """Step 4: returns the accounts that have this profile."""
        return UserAccount.getAccountsByProfile(profileKey)

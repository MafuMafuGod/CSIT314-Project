"""«Control» SearchUserProfileController — #51 Search User Profile."""
from entity import UserProfile
from control.view_user_profile_controller import addUserCounts


class SearchUserProfileController:
    """Gets the profiles matching the search criteria from the Entities."""

    def searchUserProfiles(self, q: str, status: str) -> list:
        """Step 4: returns userProfiles with user counts (empty = none match, 4a)."""
        return addUserCounts(UserProfile.searchProfiles(q, status))

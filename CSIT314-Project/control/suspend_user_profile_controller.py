"""«Control» SuspendUserProfileController — #50 Suspend User Profile."""
from entity import UserProfile


class SuspendUserProfileController:
    """Suspends the chosen profile."""

    def suspendUserProfile(self, name: str, reason: str) -> bool:
        """Step 3: returns suspended (False = missing or already suspended)."""
        return UserProfile.suspendProfile(name, reason)

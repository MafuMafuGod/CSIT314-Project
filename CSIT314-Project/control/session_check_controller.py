"""«Control» SessionCheckController — #45 step 5 / #50 step 4: sign out users who were
suspended (or whose profile was suspended) while they were logged in."""
from entity import UserAccount, UserProfile


class SessionCheckController:
    """Asks the Entities whether a logged-in user is still allowed in."""

    def isSessionBlocked(self, u: str, profile: str) -> bool:
        """True if the account or its profile has been suspended."""
        return UserAccount.isAccountSuspended(u) or UserProfile.isProfileSuspended(profile)

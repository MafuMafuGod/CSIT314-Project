"""«Control» SuspendUserAccountController — #45 Suspend User Account."""
from entity import UserAccount


class SuspendUserAccountController:
    """Suspends the chosen account."""

    def suspendUserAccount(self, u: str, reason: str) -> bool:
        """Step 5: returns suspended (False = missing or already suspended)."""
        return UserAccount.suspendAccount(u, reason)

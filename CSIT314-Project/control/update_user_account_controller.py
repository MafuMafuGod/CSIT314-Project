"""«Control» UpdateUserAccountController — #44 Update User Account."""
from entity import UserAccount


class UpdateUserAccountController:
    """Gets the account to edit, checks the new email and saves the changes."""

    def selectUserAccount(self, u: str) -> dict:
        """Step 1: returns userAccount ({} = not found)."""
        return UserAccount.selectUserAccount(u)

    def checkAccountExists(self, u: str) -> bool:
        """Step 3: is the new email already used by another account? Returns accountExists."""
        return UserAccount.accountExists(u)

    def updateUserAccount(self, u: str, name: str, newU: str, profile: str, permissions: list) -> bool:
        """Step 4: returns updated from the Entity."""
        return UserAccount.updateAccount(u, name, newU, profile, permissions)

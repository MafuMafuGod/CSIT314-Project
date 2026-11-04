"""«Control» SearchUserAccountController — #46 Search User Account."""
from entity import UserAccount


class SearchUserAccountController:
    """Gets the accounts matching the search criteria from the Entity."""

    def searchUserAccounts(self, q: str, status: str, profile: str) -> list:
        """Step 5: returns userAccounts (empty = no matching accounts, 7a)."""
        return UserAccount.searchAccounts(q, status, profile)

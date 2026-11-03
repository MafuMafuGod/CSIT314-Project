"""«Control» ViewUserAccountController — #43 View User Account."""
from entity import UserAccount


class ViewUserAccountController:
    """Gets the account list and a selected account's details from the Entity."""

    def getUserAccountList(self) -> list:
        """Step 1: returns userAccounts."""
        return UserAccount.getAllAccounts()

    def selectUserAccount(self, u: str) -> dict:
        """Steps 2-3: returns userAccount."""
        return UserAccount.selectUserAccount(u)

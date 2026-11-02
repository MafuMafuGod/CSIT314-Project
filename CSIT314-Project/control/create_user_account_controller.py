"""«Control» CreateUserAccountController — #42 Create User Account."""
from entity import UserAccount


class CreateUserAccountController:
    """Checks stored data and creates the account. Input validation is done by the Boundary."""

    def checkAccountExists(self, u: str) -> bool:
        """Step 6b: returns accountExists from the Entity."""
        return UserAccount.accountExists(u)

    def createUserAccount(self, name: str, u: str, p: str, profile: str) -> bool:
        """Step 7: returns accountCreated from the Entity."""
        return UserAccount.createAccount(name, u, p, profile)

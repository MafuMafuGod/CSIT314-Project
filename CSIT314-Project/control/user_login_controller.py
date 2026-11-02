"""«Control» UserLoginController — #06 User Login, #31 Customer Login, #70 Platform Admin Login."""
from entity import UserAccount


class UserLoginController:
    """Receives requests from the Boundary and applies them to the Entity."""

    def userAccountLogin(self, u: str, p: str) -> bool:
        """Step 5: returns loginSuccess (True / False) from the Entity."""
        return UserAccount.userAccountLogin(u, p)

    def getUserProfile(self, u: str) -> str:
        """Step 6: returns profile from the Entity."""
        return UserAccount.getProfile(u)

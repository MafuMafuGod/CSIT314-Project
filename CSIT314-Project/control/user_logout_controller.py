"""«Control» UserLogoutController — #07 User Logout, #37 Customer Logout."""
from entity import UserSession


class UserLogoutController:
    """Receives the logout request from the Boundary and applies it to the Entity."""

    def userAccountLogout(self) -> bool:
        """Step 2: returns logoutSuccess from the Entity."""
        return UserSession().killSession()

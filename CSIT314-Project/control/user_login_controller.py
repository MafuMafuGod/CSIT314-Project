"""«Control» 
UserLoginController — #06 User Login, #14 Interior Designer Login, #31 Customer Login,
#70 Platform Admin Login."""
from entity import UserAccount, UserProfile

# Passes the page's request to the Entity and returns the answer
class UserLoginController:
    """Receives requests from the Boundary and applies them to the Entity."""

    def userAccountLogin(self, u: str, p: str) -> bool:
        """Step 5: returns loginSuccess (True / False)
        Fails for wrong credentials, a suspended account (#45) or a suspended profile (#50)"""
        loginSuccess = (UserAccount.userAccountLogin(u, p)
                        and not UserProfile.isProfileSuspended(UserAccount.getProfile(u)))
        # remember the time of this successful sign-in
        if loginSuccess:
            UserAccount.recordSignIn(u)
        return loginSuccess

    def getUserProfile(self, u: str) -> str:
        """Step 6: returns profile from the Entity."""
        return UserAccount.getProfile(u)

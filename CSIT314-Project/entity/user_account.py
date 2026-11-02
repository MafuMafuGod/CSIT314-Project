"""«Entity» UserAccount — used by #06 Login, #42 Create User Account, #43 View User Account."""
from typing import Optional


class UserAccount:
    """A registered user account. Owns the account data and checks credentials."""

    _accounts = []                      # stand-in for the database table

    def __init__(self, name: str, u: str, p: str, profile: str, status: str = "active") -> None:
        self._name = name                # full name
        self._u = u                      # username (email)
        self._p = p                      # password
        self._profile = profile                # customer / designer / admin / platform
        self._status = status            # active / suspended

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findAccount(cls, u: str) -> Optional["UserAccount"]:
        for account in cls._accounts:
            if account._u == u:
                return account
        return None

    def _toDict(self) -> dict:
        """Account details for display (password is never included)."""
        return {"name": self._name, "u": self._u, "profile": self._profile, "status": self._status}

    # ---- #06 User Login ------------------------------------------------------
    @classmethod
    def userAccountLogin(cls, u: str, p: str) -> bool:
        """#06 step 5: verify credentials against the stored accounts."""
        account = cls._findAccount(u)
        return account is not None and account._p == p

    @classmethod
    def getProfile(cls, u: str) -> str:
        """#06 step 6: return the user's assigned profile."""
        account = cls._findAccount(u)
        return account._profile if account else ""

    # ---- #42 Create User Account --------------------------------------------
    @classmethod
    def accountExists(cls, u: str) -> bool:
        """#42 step 6b: is this email already registered?"""
        return cls._findAccount(u) is not None

    @classmethod
    def createAccount(cls, name: str, u: str, p: str, profile: str) -> bool:
        """#42 step 7: store the new account."""
        cls._accounts.append(UserAccount(name, u, p, profile))
        return True

    # ---- #43 View User Account ----------------------------------------------
    @classmethod
    def getAllAccounts(cls) -> list:
        """#43 step 1: return every account, for the User Management list."""
        return [account._toDict() for account in cls._accounts]

    @classmethod
    def selectUserAccount(cls, u: str) -> dict:
        """#43 step 3: return one account's details ({} if not found)."""
        account = cls._findAccount(u)
        return account._toDict() if account else {}


# Sample data
UserAccount._accounts = [
    UserAccount("Hannah Tan", "customer@4reno.com", "password123", "customer"),
    UserAccount("Daniel Lim", "designer@4reno.com", "design123", "designer"),
    UserAccount("Alex Wong", "admin@4reno.com", "admin123", "admin"),
    UserAccount("Priya Nair", "platform@4reno.com", "platform123", "platform"),
]

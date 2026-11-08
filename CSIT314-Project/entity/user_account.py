"""«Entity» UserAccount — used by #06 / #14 / #31 / #70 Login, #42 Create, #43 View, #44 Update,
#45 Suspend and #46 Search User Account."""
from datetime import date, datetime
from typing import Optional


class UserAccount:
    """A registered user account. Owns the account data and checks credentials."""

    _accounts = []                      # stand-in for the database table
    _nextUserID = 1

    def __init__(self, name: str, u: str, p: str, profile: str, permissions: list = None,
                 status: str = "active", createdAt: str = "") -> None:
        self._userID = UserAccount._nextUserID
        UserAccount._nextUserID += 1
        self._name = name                # full name
        self._u = u                      # username (email)
        self._p = p                      # password
        self._profile = profile          # profile key, e.g. "designer" (see UserProfile)
        self._permissions = list(permissions or [])
        self._status = status            # active / suspended
        self._createdAt = createdAt or date.today().isoformat()
        self._lastSignIn = ""
        self._suspendedOn = ""
        self._suspendReason = ""

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findAccount(cls, u: str) -> Optional["UserAccount"]:
        u = u.lower()
        for account in cls._accounts:
            if account._u.lower() == u:
                return account
        return None

    def _toDict(self) -> dict:
        """Account details for display (password is never included)."""
        return {"userID": self._userID, "name": self._name, "u": self._u,
                "profile": self._profile, "permissions": list(self._permissions),
                "status": self._status, "created_at": self._createdAt,
                "lastSignIn": self._lastSignIn, "suspendedOn": self._suspendedOn,
                "suspendReason": self._suspendReason}

    # ---- #06 / #14 / #31 / #70 Login ----------------------------------------------
    @classmethod
    def userAccountLogin(cls, u: str, p: str) -> bool:
        """#06 step 5 / #14 / #31 step 6 / #70: verify credentials. A suspended account cannot
        log in (#45 step 6)."""
        account = cls._findAccount(u)
        return account is not None and account._p == p and account._status == "active"

    @classmethod
    def getProfile(cls, u: str) -> str:
        """#06 step 6 / #14 / #31 step 7 / #70: return the user's assigned profile."""
        account = cls._findAccount(u)
        return account._profile if account else ""

    @classmethod
    def recordSignIn(cls, u: str) -> bool:
        """After a successful login: shown as "Last sign-in" on #43 / #46."""
        account = cls._findAccount(u)
        if account is None:
            return False
        account._lastSignIn = datetime.now().strftime("%Y-%m-%d %H:%M")
        return True

    @classmethod
    def isAccountSuspended(cls, u: str) -> bool:
        """Session check: a suspended account is signed out on its next page load (#45 step 5)."""
        account = cls._findAccount(u)
        return account is not None and account._status == "suspended"

    # ---- #42 Create User Account --------------------------------------------
    @classmethod
    def accountExists(cls, u: str) -> bool:
        """#42 step 6b / #44: is this email already registered? (not case-sensitive)"""
        return cls._findAccount(u) is not None

    @classmethod
    def createAccount(cls, name: str, u: str, p: str, profile: str, permissions: list = None) -> bool:
        """#42 step 7: store the new account."""
        cls._accounts.append(UserAccount(name, u, p, profile, permissions))
        return True

    # ---- #43 View User Account ----------------------------------------------
    @classmethod
    def getAllAccounts(cls) -> list:
        """#43 step 1: return every account, for the User Management list."""
        return [account._toDict() for account in cls._accounts]

    @classmethod
    def selectUserAccount(cls, u: str) -> dict:
        """#43 step 3 / #44: return one account's details ({} if not found)."""
        account = cls._findAccount(u)
        return account._toDict() if account else {}

    # ---- #44 Update User Account --------------------------------------------
    @classmethod
    def updateAccount(cls, u: str, name: str, newU: str, profile: str, permissions: list) -> bool:
        """#44 step 4: save the updated details. False if the account no longer exists."""
        account = cls._findAccount(u)
        if account is None:
            return False
        account._name = name
        account._u = newU
        account._profile = profile
        account._permissions = list(permissions)
        return True

    # ---- #45 Suspend User Account -------------------------------------------
    @classmethod
    def suspendAccount(cls, u: str, reason: str) -> bool:
        """#45 step 5: set the status to suspended. False if missing or already suspended."""
        account = cls._findAccount(u)
        if account is None or account._status == "suspended":
            return False
        account._status = "suspended"
        account._suspendedOn = date.today().isoformat()
        account._suspendReason = reason
        return True

    # ---- #46 Search User Account --------------------------------------------
    @classmethod
    def searchAccounts(cls, q: str, status: str, profile: str) -> list:
        """#46 step 5: name or email contains q (not case-sensitive), status and profile
        match. Empty criteria mean "any". [] if nothing matches (7a)."""
        q = q.lower()
        return [a._toDict() for a in cls._accounts
                if (not q or q in a._name.lower() or q in a._u.lower())
                and (not status or a._status == status)
                and (not profile or a._profile == profile)]

    # ---- #48 / #50: accounts that use a profile ------------------------------
    @classmethod
    def getAccountsByProfile(cls, profile: str) -> list:
        """#48 step 4: the users who have this profile."""
        return [a._toDict() for a in cls._accounts if a._profile == profile]

    @classmethod
    def countAccountsByProfile(cls) -> dict:
        """#48 / #51: {profile key: number of accounts}."""
        counts = {}
        for a in cls._accounts:
            counts[a._profile] = counts.get(a._profile, 0) + 1
        return counts


# Sample data
UserAccount._accounts = [
    UserAccount("Hannah Tan", "customer@4reno.com", "password123", "customer",
                ["Search IDPs", "View IDP details", "Manage shortlist"], createdAt="2026-10-02"),
    UserAccount("Daniel Lim", "designer@4reno.com", "design123", "designer",
                ["Manage own IDPs", "View IDP view count", "View IDP shortlist count"], createdAt="2026-10-02"),
    UserAccount("Alex Wong", "admin@4reno.com", "admin123", "admin",
                ["Manage user accounts", "Manage user profiles", "View audit log"], createdAt="2026-10-01"),
    UserAccount("Priya Nair", "platform@4reno.com", "platform123", "platform",
                ["Access IDP database"], createdAt="2026-10-01"),
]

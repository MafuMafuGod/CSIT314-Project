"""«Entity» UserProfile — a role and the permissions it grants.
Used by #42 / #44 (profile choices), #47 Create, #48 View, #49 Update, #50 Suspend,
#51 Search User Profile, and by login (#06 / #31 / #70) to block suspended profiles."""
import re
from datetime import date
from typing import Optional


class UserProfile:
    """A user profile (role). Accounts point to it through its key, e.g. "designer"."""

    # Every permission that exists in the system, grouped for display (#47 precondition)
    PERMISSION_GROUPS = {
        "Customers": ["Search IDPs", "View IDP details", "Manage shortlist"],
        "Interior Designers": ["Manage own IDPs", "View IDP view count", "View IDP shortlist count"],
        "Administration": ["Manage user accounts", "Manage user profiles", "View audit log"],
        "Platform Management": ["Access IDP database"],
    }

    _profiles = []                      # stand-in for the database table

    def __init__(self, key: str, name: str, description: str, permissions: list,
                 status: str = "active", created: str = "") -> None:
        self._key = key                  # stored in UserAccount and the session, never changes
        self._name = name                # shown to users, can be renamed (#49)
        self._description = description
        self._permissions = list(permissions)
        self._status = status            # active / suspended
        self._created = created or date.today().isoformat()
        self._suspendedOn = ""
        self._suspendReason = ""

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findByName(cls, name: str) -> Optional["UserProfile"]:
        name = name.strip().lower()
        for profile in cls._profiles:
            if profile._name.lower() == name:
                return profile
        return None

    @classmethod
    def _findByKey(cls, key: str) -> Optional["UserProfile"]:
        for profile in cls._profiles:
            if profile._key == key:
                return profile
        return None

    @classmethod
    def _makeKey(cls, name: str) -> str:
        """A unique key from the name, e.g. "Senior Admin" -> "senior-admin"."""
        base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "profile"
        key, n = base, 2
        while cls._findByKey(key):
            key, n = f"{base}-{n}", n + 1
        return key

    def _toDict(self) -> dict:
        return {"key": self._key, "name": self._name, "description": self._description,
                "permissions": list(self._permissions), "status": self._status,
                "created": self._created, "suspendedOn": self._suspendedOn,
                "suspendReason": self._suspendReason}

    # ---- shared lookups (profile choices, labels, permissions) -------------
    @classmethod
    def getPermissionGroups(cls) -> dict:
        """Every permission in the system, grouped."""
        return {group: list(perms) for group, perms in cls.PERMISSION_GROUPS.items()}

    @classmethod
    def getProfileLabels(cls) -> dict:
        """{key: name} for every profile, e.g. {"designer": "Interior Designer"}."""
        return {p._key: p._name for p in cls._profiles}

    @classmethod
    def getActiveProfileOptions(cls) -> dict:
        """{key: name} for profiles that can be given to an account (not suspended)."""
        return {p._key: p._name for p in cls._profiles if p._status == "active"}

    @classmethod
    def getProfileDefaults(cls) -> dict:
        """{key: permissions}: ticked automatically when a profile is picked for an account."""
        return {p._key: list(p._permissions) for p in cls._profiles}

    @classmethod
    def isProfileSuspended(cls, key: str) -> bool:
        """Login and session check: users whose profile is suspended are blocked (#50 step 4)."""
        profile = cls._findByKey(key)
        return profile is not None and profile._status == "suspended"

    @classmethod
    def getProfileNames(cls) -> list:
        return [p._name for p in cls._profiles]

    # ---- #47 Create User Profile --------------------------------------------
    @classmethod
    def profileNameExists(cls, name: str) -> bool:
        """#47 step 8 / #49: is the name taken? (not case-sensitive)"""
        return cls._findByName(name) is not None

    @classmethod
    def createProfile(cls, name: str, description: str, permissions: list) -> bool:
        """#47 steps 9-10: store the new profile with its permissions."""
        cls._profiles.append(UserProfile(cls._makeKey(name), name, description, permissions))
        return True

    # ---- #48 View User Profile ----------------------------------------------
    @classmethod
    def getAllProfiles(cls) -> list:
        """#48 step 2: every profile. [] if none exist (5a)."""
        return [p._toDict() for p in cls._profiles]

    @classmethod
    def selectProfile(cls, name: str) -> dict:
        """#48 step 4: one profile's details and permissions ({} if not found)."""
        profile = cls._findByName(name)
        return profile._toDict() if profile else {}

    # ---- #49 Update User Profile --------------------------------------------
    @classmethod
    def updateProfile(cls, name: str, newName: str, description: str, permissions: list) -> bool:
        """#49 step 5: save the changes. False if the profile no longer exists (8a)."""
        profile = cls._findByName(name)
        if profile is None:
            return False
        profile._name = newName
        profile._description = description
        profile._permissions = list(permissions)
        return True

    # ---- #50 Suspend User Profile -------------------------------------------
    @classmethod
    def suspendProfile(cls, name: str, reason: str) -> bool:
        """#50 step 3: set the status to suspended. False if missing or already suspended."""
        profile = cls._findByName(name)
        if profile is None or profile._status == "suspended":
            return False
        profile._status = "suspended"
        profile._suspendedOn = date.today().isoformat()
        profile._suspendReason = reason
        return True

    # ---- #51 Search User Profile --------------------------------------------
    @classmethod
    def searchProfiles(cls, q: str, status: str) -> list:
        """#51 step 4: name contains q (not case-sensitive) and status matches.
        Empty q or status means "any". [] if nothing matches (4a)."""
        q = q.lower()
        return [p._toDict() for p in cls._profiles
                if (not q or q in p._name.lower()) and (not status or p._status == status)]


# Sample data: the four profiles the platform starts with
UserProfile._profiles = [
    UserProfile("customer", "Customer", "Homeowners looking for an interior designer",
                UserProfile.PERMISSION_GROUPS["Customers"], created="2026-10-01"),
    UserProfile("designer", "Interior Designer", "Designers who publish IDPs",
                UserProfile.PERMISSION_GROUPS["Interior Designers"], created="2026-10-01"),
    UserProfile("admin", "User Admin", "Manages user accounts and profiles",
                UserProfile.PERMISSION_GROUPS["Administration"], created="2026-10-01"),
    UserProfile("platform", "Platform Management", "Runs the IDP platform and its database",
                UserProfile.PERMISSION_GROUPS["Platform Management"], created="2026-10-01"),
]

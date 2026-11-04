"""«Entity» UserSession — used by #07 / #37 Logout."""
from flask import session


class UserSession:
    """The logged-in user's active session (the u and profile saved at login)."""

    def __init__(self) -> None:
        self._u = session.get("u", "")
        self._profile = session.get("profile", "")

    def killSession(self) -> bool:
        """Step 3: terminate the active session. Returns logoutSuccess.
        No "is anyone logged in?" check here: the requireLogin guard in app.py
        (precondition) already guarantees a user is logged in."""
        session.clear()
        return True

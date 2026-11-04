"""Shared helpers for the user account / user profile tests."""
import copy

from entity import UserAccount, UserProfile


def snapshot():
    return copy.deepcopy(UserAccount._accounts), copy.deepcopy(UserProfile._profiles), UserAccount._nextUserID


def restore(saved):
    UserAccount._accounts, UserProfile._profiles, UserAccount._nextUserID = saved


def loggedIn(appModule, u, p):
    client = appModule.app.test_client()
    with client.session_transaction() as s:
        s["csrf"] = "t"
    client.post("/login", data={"u": u, "p": p, "csrf_token": "t"})
    return client


def post(client, url, **data):
    data["csrf_token"] = "t"
    return client.post(url, data=data, follow_redirects=True).get_data(as_text=True)

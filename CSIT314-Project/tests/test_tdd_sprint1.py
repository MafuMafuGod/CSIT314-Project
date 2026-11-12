"""
TDD for Sprint 1: Login and Logout for every profile

    Login  : #06 User Admin, #14 Interior Designer, #31 Customer, #70 Platform Management
    Logout : #07 User Admin, #15 Interior Designer, #37 Customer, #71 Platform Management

All four profiles use the same login page, the same controllers and the same entities,
so each test below is run once for every profile (the ROLES list).

Cycle 1: validateFields(u, p)            Boundary, login alternate flow (empty fields)
Cycle 2: UserAccount.getProfile(u)       Entity, login step "check the user's profile"
Cycle 3: UserSession.killSession()       Entity, logout steps "end the session"
Cycle 4: case-sensitive login            Entity + Boundary

Run one cycle:    python tdd_runner.py tests.test_tdd_sprint1.ValidateFieldsTest
Run all cycles:   python tdd_runner.py tests.test_tdd_sprint1
"""
import os
import sys
import unittest

from flask import session

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                        # the Flask app
from boundary.user_login_page import validateFields             # Cycle 1: function we are testing
from entity import UserAccount, UserSession                     # Cycles 2, 3, 4: Entities we are testing

# One row per profile: (login story, logout story, role name, email, password, profile key)
ROLES = [
    ("#06", "#07", "User Admin",          "admin@4reno.com",    "admin123",    "admin"),
    ("#14", "#15", "Interior Designer",   "designer@4reno.com", "design123",   "designer"),
    ("#31", "#37", "Customer",            "customer@4reno.com", "password123", "customer"),
    ("#70", "#71", "Platform Management", "platform@4reno.com", "platform123", "platform"),
]


# ---------------------------------------------------------------- Cycle 1
class ValidateFieldsTest(unittest.TestCase):
    longMessage = False          # show only our own failure message

    def testAllFieldsFilled(self):
        # both fields filled -> nothing is missing
        for story, _, role, email, password, _ in ROLES:
            with self.subTest(story=story):
                actual = validateFields(email, password)
                self.assertEqual([], actual, f"{role} all filled expected:<[]> but was:<{actual}>")

    def testEmailMissing(self):
        # empty email -> "u" (the username/email field) is missing
        for story, _, role, _, password, _ in ROLES:
            with self.subTest(story=story):
                actual = validateFields("", password)
                self.assertEqual(["u"], actual, f"{role} email missing expected:<['u']> but was:<{actual}>")

    def testPasswordMissing(self):
        # empty password -> "p" is missing
        for story, _, role, email, _, _ in ROLES:
            with self.subTest(story=story):
                actual = validateFields(email, "")
                self.assertEqual(["p"], actual, f"{role} password missing expected:<['p']> but was:<{actual}>")

    def testBothMissing(self):
        # both empty -> both fields are missing, email first
        actual = validateFields("", "")
        self.assertEqual(["u", "p"], actual, f"Both missing expected:<['u', 'p']> but was:<{actual}>")


# ---------------------------------------------------------------- Cycle 2
class ProfileAfterLoginTest(unittest.TestCase):
    longMessage = False

    def testEachRoleGetsItsOwnProfile(self):
        # the Entity must return the profile saved for each account
        for story, _, role, email, _, profile in ROLES:
            with self.subTest(story=story):
                actual = UserAccount.getProfile(email)
                self.assertEqual(profile, actual, f"{role} profile expected:<{profile}> but was:<{actual}>")

    def testUnknownEmailHasNoProfile(self):
        # an email that is not registered has no profile
        actual = UserAccount.getProfile("nobody@4reno.com")
        self.assertEqual("", actual, f"Unknown email expected:<> but was:<{actual}>")

    def testSessionHoldsProfileAfterLogin(self):
        # log in through the login page, then look at what the session remembers
        app_module.app.config["TESTING"] = True
        for story, _, role, email, password, profile in ROLES:
            with self.subTest(story=story):
                with app_module.app.test_client() as browser:
                    browser.post("/login", data={"u": email, "p": password})
                    with browser.session_transaction() as s:
                        actual = s.get("profile")
                self.assertEqual(profile, actual, f"{role} session profile expected:<{profile}> but was:<{actual}>")


# ---------------------------------------------------------------- Cycle 3
class KillSessionTest(unittest.TestCase):
    longMessage = False

    def logIn(self, email, profile):
        # pretend this user is logged in: put u and profile in the session
        context = app_module.app.test_request_context("/")
        context.push()
        self.addCleanup(context.pop)
        session["u"] = email
        session["profile"] = profile

    def testLogoutReturnsTrue(self):
        # the Entity reports logoutSuccess = True
        for _, story, role, email, _, profile in ROLES:
            with self.subTest(story=story):
                self.logIn(email, profile)
                actual = UserSession().killSession()
                self.assertEqual(True, actual, f"{role} logout expected:<True> but was:<{actual}>")

    def testSessionIsCleared(self):
        # after logout nothing about the user is left in the session
        for _, story, role, email, _, profile in ROLES:
            with self.subTest(story=story):
                self.logIn(email, profile)
                UserSession().killSession()
                actual = dict(session)
                self.assertEqual({}, actual, f"{role} session expected:<{{}}> but was:<{actual}>")


# ---------------------------------------------------------------- Cycle 4
class CaseSensitiveLoginTest(unittest.TestCase):
    longMessage = False

    def testExactCredentialsLogIn(self):
        for story, _, role, email, password, _ in ROLES:
            with self.subTest(story=story):
                actual = UserAccount.userAccountLogin(email, password)
                self.assertEqual(True, actual, f"{role} exact credentials expected:<True> but was:<{actual}>")

    def testEmailInCapitalsIsRejected(self):
        for story, _, role, email, password, _ in ROLES:
            with self.subTest(story=story):
                actual = UserAccount.userAccountLogin(email.upper(), password)
                self.assertEqual(False, actual, f"{role} email in capitals expected:<False> but was:<{actual}>")

    def testPasswordInCapitalsIsRejected(self):
        for story, _, role, email, password, _ in ROLES:
            with self.subTest(story=story):
                actual = UserAccount.userAccountLogin(email, password.upper())
                self.assertEqual(False, actual, f"{role} password in capitals expected:<False> but was:<{actual}>")

    def testSessionHoldsStoredEmailAfterLogin(self):
        # log in, then look at what the session remembers
        app_module.app.config["TESTING"] = True
        for story, _, role, email, password, _ in ROLES:
            with self.subTest(story=story):
                with app_module.app.test_client() as browser:
                    browser.post("/login", data={"u": email, "p": password})
                    with browser.session_transaction() as s:
                        actual = s.get("u")
                self.assertEqual(email, actual, f"{role} session email expected:<{email}> but was:<{actual}>")


if __name__ == "__main__":
    unittest.main()
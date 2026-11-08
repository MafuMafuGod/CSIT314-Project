"""
TDD cycle 3: User Story #37 (Customer logs out) - UserSession.killSession()

Rule from the use case (steps 2-3): the system ends the Customer's session and
reports that the logout worked.
"""
import os
import sys
import unittest

from flask import session

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                      # the Flask app (needed for the session)
from entity import UserSession                                 # the class we are testing


class KillSessionTest(unittest.TestCase):
    longMessage = False

    def setUp(self):
        # pretend a Customer is logged in: put u and profile in the session
        self.context = app_module.app.test_request_context("/")
        self.context.push()
        session["u"] = "customer@4reno.com"
        session["profile"] = "customer"
        self.addCleanup(self.context.pop)

    def testLogoutReturnsTrue(self):
        # the Entity reports logoutSuccess = True
        actual = UserSession().killSession()
        self.assertEqual(True, actual, f"Logout expected:<True> but was:<{actual}>")

    def testSessionIsCleared(self):
        # after logout nothing about the user is left in the session
        UserSession().killSession()
        actual = dict(session)
        self.assertEqual({}, actual, f"Session expected:<{{}}> but was:<{actual}>")


if __name__ == "__main__":
    unittest.main()

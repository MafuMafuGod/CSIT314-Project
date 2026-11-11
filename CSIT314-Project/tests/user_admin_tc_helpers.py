"""Shared setup for user account/profile user-story cases TC42–TC51."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module  # noqa: E402
from tests.helpers import restore, snapshot  # noqa: E402

ADMIN_EMAIL = "admin@4reno.com"
ADMIN_PASSWORD = "admin123"


class BaseUserAdminTest(unittest.TestCase):
    """Log in as the sample User Admin and restore in-memory data after each test."""

    def setUp(self):
        self.savedData = snapshot()
        app_module.app.config["TESTING"] = True
        self.browser = self.loginAs(ADMIN_EMAIL, ADMIN_PASSWORD)

    def tearDown(self):
        restore(self.savedData)

    def loginAs(self, email, password):
        browser = app_module.app.test_client()
        browser.post("/login", data={"u": email, "p": password})
        return browser

    @staticmethod
    def clean(html):
        return " ".join(html.split())

    def getText(self, path, browser=None, follow_redirects=True):
        response = (browser or self.browser).get(path, follow_redirects=follow_redirects)
        return response, self.clean(response.get_data(as_text=True))

    def postText(self, path, data=None, browser=None, follow_redirects=True):
        response = (browser or self.browser).post(path, data=data or {}, follow_redirects=follow_redirects)
        return response, self.clean(response.get_data(as_text=True))

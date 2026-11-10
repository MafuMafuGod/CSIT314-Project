"""
Small helpers shared by the test case files TC31 - TC37.
Each test follows one row (test step) of Test_Cases_31-37.xlsx.
"""
import copy, os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                              # the Flask app
from entity import InteriorDesignProject, Shortlist, UserAccount      # the data we reset

app_module.app.config["TESTING"] = True

CUSTOMER = "customer@4reno.com"
CUSTOMER_PASSWORD = "password123"
DESIGNER = "designer@4reno.com"
DESIGNER_PASSWORD = "design123"


class BaseTest(unittest.TestCase):
    """Every test starts with the same sample data and puts it back afterwards."""

    def setUp(self):
        # keep a copy of the data so one test does not change the next test
        self.savedIDPs = copy.deepcopy(InteriorDesignProject._idps)
        self.savedShortlist = copy.deepcopy(Shortlist._entries)
        self.savedAccounts = copy.deepcopy(UserAccount._accounts)

    def tearDown(self):
        InteriorDesignProject._idps = self.savedIDPs
        Shortlist._entries = self.savedShortlist
        UserAccount._accounts = self.savedAccounts


def newBrowser():
    """A browser that is not logged in."""
    return app_module.app.test_client()


def login(email=CUSTOMER, password=CUSTOMER_PASSWORD):
    """A browser that is already logged in."""
    browser = newBrowser()
    browser.post("/login", data={"u": email, "p": password})
    return browser


def cleanText(html):
    """Squash line breaks and extra spaces so text split over two lines still matches."""
    return " ".join(html.split())


def getText(browser, url):
    """Open a page (follows redirects) and return its HTML text."""
    return cleanText(browser.get(url, follow_redirects=True).get_data(as_text=True))


def postText(browser, url, **data):
    """Click a button (POST, follows redirects) and return the HTML text."""
    return cleanText(browser.post(url, data=data, follow_redirects=True).get_data(as_text=True))


def getIDP(idpID):
    """Find an IDP object by its id (used to read counts / remove it)."""
    for idp in InteriorDesignProject._idps:
        if idp._idpID == idpID:
            return idp
    return None


def removeIDP(idpID):
    """Pretend the Interior Designer removed the IDP."""
    InteriorDesignProject._idps = [i for i in InteriorDesignProject._idps if i._idpID != idpID]

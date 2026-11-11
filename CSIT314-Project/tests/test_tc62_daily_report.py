"""
TC62 - Platform Admin Generating a Daily Report (User Story #62)
Precondition: the Platform Admin is logged in.
Each test follows one row (test step) of Matthew's test case sheet (TC62).
The sample activity is dated relative to today, so the dates below are worked out from today
(the test case sheet shows the dates as of 9 Nov 2026).
Run:  python -m unittest tests.test_tc62_daily_report -v
"""
import copy
from datetime import date, timedelta
from tests.tc_helpers import *
from entity import ProjectReport

PLATFORM = "platform@4reno.com"
PLATFORM_PASSWORD = "platform123"
SENGKANG = "4"          # Sengkang BTO Minimalist Living Room (has sample activity)
CLEMENTI = "5"          # Clementi Resale Japandi Bedroom (activity 9 and 3 days ago only)
TODAY = date.today()


def daysAgo(n):
    return (TODAY - timedelta(days=n)).isoformat()


class TC62(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedReports = copy.deepcopy(ProjectReport._reports)
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        ProjectReport._reports = self.savedReports
        super().tearDown()

    def test_TC62_1(self):
        # Platform Admin selects a project and date, clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/daily", projectID=SENGKANG, date=daysAgo(5))
        self.assertIn(f"Daily report &middot; {daysAgo(5)}", html)
        self.assertIn("Task completed: Electrical rewiring", html)
        self.assertIn("Download CSV", html)

    def test_TC62_2(self):
        # Platform Admin selects a day with no activity and clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/daily", projectID=CLEMENTI, date=daysAgo(1))
        self.assertIn("No progress records found for this day.", html)

    def test_TC62_3(self):
        # Platform Admin enters a date in the future and clicks 'Generate Report'
        tomorrow = (TODAY + timedelta(days=1)).isoformat()
        html = postText(self.browser, "/platform/reports/daily", projectID=SENGKANG, date=tomorrow)
        self.assertIn("Date cannot be in the future.", html)

    def test_TC62_4(self):
        # Platform Admin does not select a project and clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/daily", projectID="", date=daysAgo(1))
        self.assertIn("Select a project.", html)


if __name__ == "__main__":
    unittest.main()

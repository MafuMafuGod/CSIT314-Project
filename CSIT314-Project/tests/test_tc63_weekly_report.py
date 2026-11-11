"""
TC63 - Platform Admin Generating a Weekly Report (User Story #63)
Precondition: the Platform Admin is logged in.
Each test follows one row (test step) of Matthew's test case sheet (TC63).
The sample activity is dated relative to today, so the dates below are worked out from today
(the test case sheet shows the dates as of 9 Nov 2026).
Run:  python -m unittest tests.test_tc63_weekly_report -v
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


class TC63(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedReports = copy.deepcopy(ProjectReport._reports)
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        ProjectReport._reports = self.savedReports
        super().tearDown()

    def test_TC63_1(self):
        # Platform Admin selects a project and a 7-day range, clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/weekly", projectID=SENGKANG, startDate=daysAgo(6), endDate=daysAgo(0))
        self.assertIn(f"Weekly report &middot; {daysAgo(6)} to {daysAgo(0)}", html)
        self.assertIn("Download CSV", html)

    def test_TC63_2(self):
        # Platform Admin selects a week with no activity and clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/weekly", projectID=CLEMENTI, startDate=daysAgo(30), endDate=daysAgo(24))
        self.assertIn("No progress records found for this week.", html)

    def test_TC63_3(self):
        # Platform Admin selects a range longer than 7 days and clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/weekly", projectID=SENGKANG, startDate=daysAgo(20), endDate=daysAgo(0))
        self.assertIn("Choose a date range of one to seven days.", html)


if __name__ == "__main__":
    unittest.main()

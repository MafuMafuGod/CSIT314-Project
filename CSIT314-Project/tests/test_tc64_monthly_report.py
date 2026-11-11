"""
TC64 - Platform Admin Generating a Monthly Report (User Story #64)
Precondition: the Platform Admin is logged in.
Each test follows one row (test step) of Matthew's test case sheet (TC64).
The sample activity is dated relative to today, so the dates below are worked out from today
(the test case sheet shows the dates as of 9 Nov 2026).
Run:  python -m unittest tests.test_tc64_monthly_report -v
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


class TC64(BaseTest):

    def setUp(self):
        super().setUp()
        self.savedReports = copy.deepcopy(ProjectReport._reports)
        self.browser = login(PLATFORM, PLATFORM_PASSWORD)    # precondition: Platform Admin logged in

    def tearDown(self):
        ProjectReport._reports = self.savedReports
        super().tearDown()

    def test_TC64_1(self):
        # Platform Admin selects a project and this month, clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/monthly", projectID=SENGKANG, month=TODAY.strftime("%Y-%m"))
        self.assertIn(f"Monthly report &middot; {TODAY.replace(day=1).isoformat()} to {TODAY.isoformat()}", html)
        self.assertIn("Download CSV", html)

    def test_TC64_2(self):
        # Platform Admin selects a month with no activity and clicks 'Generate Report'
        html = postText(self.browser, "/platform/reports/monthly", projectID=CLEMENTI, month="2026-01")
        self.assertIn("No progress records found for this month.", html)

    def test_TC64_3(self):
        # Platform Admin selects a month in the future and clicks 'Generate Report'
        nextMonth = (TODAY.replace(day=28) + timedelta(days=5)).strftime("%Y-%m")
        html = postText(self.browser, "/platform/reports/monthly", projectID=SENGKANG, month=nextMonth)
        self.assertIn("The selected month cannot be in the future.", html)


if __name__ == "__main__":
    unittest.main()

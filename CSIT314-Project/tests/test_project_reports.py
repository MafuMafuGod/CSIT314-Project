"""
Unit tests for #62 Daily, #63 Weekly and #64 Monthly project reports (Platform Administrator).
Run from the project folder:   python -m pytest tests/test_project_reports.py -v
"""
import os
import sys
from datetime import date, datetime, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module                                                   # noqa: E402
from entity import InteriorDesignProject, ProjectReport                     # noqa: E402
from control import (DailyProjectReportController, WeeklyProjectReportController,   # noqa: E402
                     MonthlyProjectReportController, UpdateCurrentProjectController)
from boundary.project_report_page import validateReportInput                # noqa: E402
from tests.helpers import loggedIn                                          # noqa: E402

TODAY = date.today()
NOW = datetime.now().astimezone().replace(microsecond=0)


@pytest.fixture(autouse=True)
def fresh_data():
    saved = (list(InteriorDesignProject._idps), list(ProjectReport._activityLogs), dict(ProjectReport._reports))
    InteriorDesignProject._idps = [
        InteriorDesignProject(1, "designer@4reno.com", "Sengkang Living Room", "2026-10-08",
                              description="d", designs="d", materials="m"),
        InteriorDesignProject(2, "designer@4reno.com", "Quiet Project", "2026-10-08"),
    ]
    ProjectReport._activityLogs = []
    for daysAgo, eventType, summary, details in [
            (10, "issue_opened", "Issue opened: leak", {}),
            (3, "progress_changed", "Progress changed from 40% to 50%", {"oldValue": 40, "newValue": 50}),
            (0, "task_completed", "Task completed: wiring", {}),
            (0, "progress_changed", "Progress changed from 50% to 70%", {"oldValue": 50, "newValue": 70})]:
        ProjectReport.recordActivity(1, eventType, summary, details, NOW - timedelta(days=daysAgo))
    yield
    InteriorDesignProject._idps, ProjectReport._activityLogs, ProjectReport._reports = saved


@pytest.fixture
def platform():
    app_module.app.config["TESTING"] = True
    return loggedIn(app_module, "platform@4reno.com", "platform123")


def post(client, period, **data):
    return client.post(f"/platform/reports/{period}", data={"csrf_token": "t", **data}).get_data(as_text=True)


# ---------------------------------------------------------------- Entity
class TestEntity:
    def test_daily_report_summary(self):                                   # #62
        report = ProjectReport.generateReport({"projectID": 1, "name": "x", "status": "Current"},
                                              "daily", TODAY, TODAY)
        s = report["summary"]
        assert (s["tasksCompleted"], s["progressPercent"], s["progressChange"], s["activityCount"]) == (1, 70, 20, 2)
        assert s["openIssues"] == 1                                        # opened 10 days ago, still open

    def test_week_includes_earlier_progress(self):                         # #63
        s = ProjectReport.generateReport({"projectID": 1, "name": "x", "status": "Current"}, "weekly",
                                         TODAY - timedelta(days=6), TODAY)["summary"]
        assert s["progressChange"] == 30 and s["activityCount"] == 3

    def test_no_records_returns_empty(self):
        assert ProjectReport.generateReport({"projectID": 2, "name": "q", "status": "Current"},
                                            "daily", TODAY, TODAY) == {}

    def test_csv(self):
        report = ProjectReport.generateReport({"projectID": 1, "name": "Sengkang", "status": "Current"},
                                              "daily", TODAY, TODAY)
        csv = ProjectReport.getReportCSV(report["reportID"])
        assert csv.startswith("Project report,Daily") and "Task completed: wiring" in csv
        assert ProjectReport.getReportCSV("missing") == ""


# ---------------------------------------------------------------- Control
class TestControllers:
    def test_periods(self):                                                # inheritance
        assert [c.PERIOD for c in (DailyProjectReportController, WeeklyProjectReportController,
                                   MonthlyProjectReportController)] == ["daily", "weekly", "monthly"]

    def test_projects_from_idp_entity(self):
        assert [p["name"] for p in DailyProjectReportController().getProjects()] == \
            ["Quiet Project", "Sengkang Living Room"]

    def test_missing_project(self):
        assert DailyProjectReportController().generateReport(999, TODAY, TODAY)["project"] == {}

    def test_portfolio_update_is_recorded(self):                           # #54 -> reports
        UpdateCurrentProjectController().updateProject("designer@4reno.com", 2, "Quiet", "d", "d", "m", "")
        report = DailyProjectReportController().generateReport(2, TODAY, TODAY)["report"]
        assert report["activities"][0]["summary"] == "Portfolio information updated"


# ---------------------------------------------------------------- Boundary validation
class TestValidation:
    def test_daily(self):
        assert validateReportInput("daily", {"projectID": "1", "date": TODAY.isoformat()})[3] == {}
        errors = validateReportInput("daily", {"projectID": "", "date": (TODAY + timedelta(days=1)).isoformat()})[3]
        assert set(errors) == {"projectID", "date"}

    def test_weekly_range(self):
        ok = {"projectID": "1", "startDate": (TODAY - timedelta(days=6)).isoformat(), "endDate": TODAY.isoformat()}
        assert validateReportInput("weekly", ok)[3] == {}
        assert "endDate" in validateReportInput("weekly", {**ok, "startDate": (TODAY - timedelta(days=7)).isoformat()})[3]
        assert "endDate" in validateReportInput("weekly", {**ok, "startDate": TODAY.isoformat(),
                                                           "endDate": (TODAY - timedelta(days=1)).isoformat()})[3]

    def test_monthly(self):
        _, start, end, errors = validateReportInput("monthly", {"projectID": "1", "month": TODAY.isoformat()[:7]})
        assert errors == {} and start.day == 1 and end == TODAY
        assert "month" in validateReportInput("monthly", {"projectID": "1", "month": "2026-13"})[3]
        assert "month" in validateReportInput("monthly", {"projectID": "1", "month": f"{TODAY.year + 1}-01"})[3]


# ---------------------------------------------------------------- Boundary pages
class TestPages:
    def test_daily_report_page(self, platform):                            # #62
        html = post(platform, "daily", projectID="1", date=TODAY.isoformat())
        assert "Sengkang Living Room" in html and "Task completed: wiring" in html and "Download" in html

    def test_weekly_report_page(self, platform):                           # #63
        html = post(platform, "weekly", projectID="1", startDate=(TODAY - timedelta(days=6)).isoformat(),
                    endDate=TODAY.isoformat())
        assert "+30%" in html

    def test_monthly_no_records(self, platform):                           # #64
        assert "No progress records found for this month." in post(platform, "monthly", projectID="2",
                                                                   month=TODAY.isoformat()[:7])

    def test_errors_shown(self, platform):
        assert "Select a project." in post(platform, "daily", projectID="", date=TODAY.isoformat())

    def test_download(self, platform):
        post(platform, "daily", projectID="1", date=TODAY.isoformat())
        reportID = next(iter(ProjectReport._reports))
        r = platform.get(f"/platform/reports/daily/download/{reportID}")
        assert r.status_code == 200 and r.mimetype == "text/csv"

    def test_only_platform_admin(self):                                    # precondition (app.py guard)
        designer = loggedIn(app_module, "designer@4reno.com", "design123")
        assert designer.get("/platform/reports/daily").status_code == 302
        r = app_module.app.test_client().get("/platform/reports/daily")
        assert r.status_code == 302 and "/login" in r.headers["Location"]

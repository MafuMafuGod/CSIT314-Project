"""«Entity» ProjectReport — project activity records and the reports compiled from them.
Used by #62 Daily, #63 Weekly and #64 Monthly project reports, and by #54 / #59
(updating a portfolio is recorded as activity). In-memory demo storage."""
import csv
import io
import secrets
from datetime import date, datetime, timedelta


class ProjectReport:
    """Stores progress events per project and compiles them into reports."""

    _activityLogs = []                  # stand-in for the activity table
    _reports = {}                       # generated reports, kept so they can be downloaded
    _nextLogID = 1

    # ---- recording activity --------------------------------------------------
    @classmethod
    def recordActivity(cls, projectID: int, eventType: str, summary: str, details: dict = None,
                       timestamp: datetime = None) -> bool:
        """Record one event for a project (called by a Controller)."""
        occurred = timestamp or datetime.now().astimezone()
        cls._activityLogs.append({"logID": cls._nextLogID, "projectID": projectID,
                                  "timestamp": occurred.isoformat(timespec="seconds"),
                                  "eventType": eventType, "summary": summary,
                                  "details": dict(details or {})})
        cls._nextLogID += 1
        return True

    # ---- #62 / #63 / #64 -----------------------------------------------------
    @classmethod
    def _logsFor(cls, projectID: int, start: date, end: date) -> list:
        rows = [dict(r) for r in cls._activityLogs if r["projectID"] == projectID
                and start <= date.fromisoformat(r["timestamp"][:10]) <= end]
        return sorted(rows, key=lambda r: (r["timestamp"], r["logID"]))

    @classmethod
    def generateReport(cls, project: dict, period: str, start: date, end: date) -> dict:
        """Compile the project's activity between start and end. {} if there is none."""
        logs = cls._logsFor(project["projectID"], start, end)
        if not logs:
            return {}
        history = cls._logsFor(project["projectID"], date.min, end)
        progress = [r for r in history if r["eventType"] == "progress_changed"]
        periodProgress = [r for r in logs if r["eventType"] == "progress_changed"]
        progressChange = None
        if periodProgress:
            progressChange = periodProgress[-1]["details"]["newValue"] - periodProgress[0]["details"]["oldValue"]
        openIssues = 0
        for r in history:
            if r["eventType"] == "issue_opened":
                openIssues += 1
            elif r["eventType"] == "issue_resolved":
                openIssues = max(0, openIssues - 1)
        summary = {
            "tasksCompleted": sum(r["eventType"] == "task_completed" for r in logs),
            "progressPercent": progress[-1]["details"]["newValue"] if progress else None,
            "progressChange": progressChange,
            "openIssues": openIssues,
            "milestonesCompleted": sum(r["eventType"] == "milestone_completed" for r in logs),
            "activityCount": len(logs),
        }
        report = {"reportID": secrets.token_urlsafe(12), "period": period,
                  "startDate": start.isoformat(), "endDate": end.isoformat(),
                  "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
                  "project": dict(project), "summary": summary, "activities": logs}
        cls._reports[report["reportID"]] = report
        return report

    @classmethod
    def getReportCSV(cls, reportID: str) -> str:
        """The report as CSV text for download ("" if it no longer exists)."""
        report = cls._reports.get(reportID)
        if not report:
            return ""
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow(["Project report", report["period"].title()])
        for label, value in (("Project ID", report["project"]["projectID"]), ("Project", report["project"]["name"]),
                             ("Status", report["project"]["status"]), ("Period start", report["startDate"]),
                             ("Period end", report["endDate"]), ("Generated at", report["generatedAt"])):
            writer.writerow([label, value])
        writer.writerow([])
        for label, key in (("Tasks completed", "tasksCompleted"), ("Progress percent", "progressPercent"),
                           ("Progress change", "progressChange"), ("Open issues", "openIssues"),
                           ("Milestones completed", "milestonesCompleted"), ("Activities", "activityCount")):
            writer.writerow([label, report["summary"][key]])
        writer.writerow([])
        writer.writerow(["Timestamp", "Activity type", "Summary"])
        for r in report["activities"]:
            writer.writerow([r["timestamp"], r["eventType"], r["summary"]])
        return stream.getvalue()


# Sample activity for the two current projects (4 and 5), dated from today so the daily,
# weekly and monthly reports all have something to show.
def _addSampleActivity():
    now = datetime.now().astimezone().replace(microsecond=0)
    samples = [
        (4, 20, "progress_changed", "Progress changed from 30% to 45%", {"oldValue": 30, "newValue": 45}),
        (4, 20, "milestone_completed", "Milestone completed: Hacking and demolition", {}),
        (4, 12, "issue_opened", "Issue opened: Ceiling leak found in living room", {}),
        (4, 5, "task_completed", "Task completed: Electrical rewiring", {}),
        (4, 5, "progress_changed", "Progress changed from 45% to 60%", {"oldValue": 45, "newValue": 60}),
        (4, 2, "issue_resolved", "Issue resolved: Ceiling leak found in living room", {}),
        (4, 0, "task_completed", "Task completed: Carpentry measurements", {}),
        (4, 0, "progress_changed", "Progress changed from 60% to 65%", {"oldValue": 60, "newValue": 65}),
        (5, 9, "task_completed", "Task completed: Moodboard approved by client", {}),
        (5, 3, "progress_changed", "Progress changed from 0% to 15%", {"oldValue": 0, "newValue": 15}),
    ]
    for projectID, daysAgo, eventType, summary, details in samples:
        ProjectReport.recordActivity(projectID, eventType, summary, details, now - timedelta(days=daysAgo))


_addSampleActivity()

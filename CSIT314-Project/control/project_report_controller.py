"""«Control» DailyProjectReportController (#62), WeeklyProjectReportController (#63) and
MonthlyProjectReportController (#64). They only differ in PERIOD (inheritance)."""
from abc import ABC
from datetime import date

from entity import InteriorDesignProject, ProjectReport


class ProjectReportController(ABC):
    """Shared by #62-#64. Each subclass sets PERIOD."""

    PERIOD = ""

    def getProjects(self) -> list:
        """Every project, for the report form."""
        return InteriorDesignProject.getProjectSummaries()

    def generateReport(self, projectID: int, start: date, end: date) -> dict:
        """Returns {"project": ..., "report": ...}: project {} = not found,
        report {} = no progress records in the period."""
        project = InteriorDesignProject.getProjectSummary(projectID)
        if not project:
            return {"project": {}, "report": {}}
        return {"project": project, "report": ProjectReport.generateReport(project, self.PERIOD, start, end)}

    def getReportCSV(self, reportID: str) -> str:
        """Returns the report as CSV ("" = no longer available)."""
        return ProjectReport.getReportCSV(reportID)


class DailyProjectReportController(ProjectReportController):
    """#62 Daily project report."""
    PERIOD = "daily"


class WeeklyProjectReportController(ProjectReportController):
    """#63 Weekly project report."""
    PERIOD = "weekly"


class MonthlyProjectReportController(ProjectReportController):
    """#64 Monthly project report."""
    PERIOD = "monthly"

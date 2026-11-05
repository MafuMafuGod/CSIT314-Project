"""«Boundary» ProjectReportPage — #62 Daily, #63 Weekly and #64 Monthly project reports
(no class: project_reports.html + route functions).
Precondition (logged-in Platform Administrator) is enforced by requirePlatform() in app.py."""
from calendar import monthrange
from datetime import date
from io import BytesIO

from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file

from control import (DailyProjectReportController, WeeklyProjectReportController,
                     MonthlyProjectReportController)

project_reports = Blueprint("project_reports", __name__)

CONTROLLERS = {"daily": DailyProjectReportController, "weekly": WeeklyProjectReportController,
               "monthly": MonthlyProjectReportController}
NO_DATA_MESSAGES = {"daily": "No progress records found for this day.",
                    "weekly": "No progress records found for this week.",
                    "monthly": "No progress records found for this month."}


def displayDashboard(period: str, selected: dict = None, report: dict = None,
                     errors: dict = None, message: str = "") -> str:
    return render_template("project_reports.html", period=period,
                           projects=CONTROLLERS[period]().getProjects(), selected=selected or {},
                           report=report or {}, errors=errors or {}, message=message,
                           today=date.today().isoformat(), active="reports")


def parsePastDate(value: str, label: str):
    """A real YYYY-MM-DD date that is not in the future. Returns (date, error)."""
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None, f"{label} must be a valid date."
    if parsed > date.today():
        return None, f"{label} cannot be in the future."
    return parsed, ""


def validateReportInput(period: str, form: dict):
    """Boundary input check: a project is chosen and the dates are valid for the period.
    Returns (projectID, start, end, errors); errors {} = all valid."""
    errors = {}
    projectID = form.get("projectID", "")
    if not projectID.isdigit():
        errors["projectID"] = "Select a project."
    start = end = None
    if period == "daily":                                               # #62: one day
        start, errors["date"] = parsePastDate(form.get("date", ""), "Date")
        end = start
    elif period == "weekly":                                            # #63: 1-7 days
        start, errors["startDate"] = parsePastDate(form.get("startDate", ""), "Week start date")
        end, errors["endDate"] = parsePastDate(form.get("endDate", ""), "Week end date")
        if start and end and (end < start or (end - start).days > 6):
            errors["endDate"] = "Choose a date range of one to seven days."
    else:                                                               # #64: one month (YYYY-MM)
        try:
            year, month = (int(x) for x in form.get("month", "").split("-"))
            start = date(year, month, 1)
            end = min(date(year, month, monthrange(year, month)[1]), date.today())
            if start > date.today():
                errors["month"] = "The selected month cannot be in the future."
        except ValueError:
            errors["month"] = "Choose a valid month."
    errors = {k: v for k, v in errors.items() if v}
    return (int(projectID) if projectID.isdigit() else 0), start, end, errors


def submitReport(period: str) -> str:
    selected = {k: v.strip() for k, v in request.form.items()}
    # Boundary validates the project and dates
    projectID, start, end, errors = validateReportInput(period, selected)
    if errors:
        return displayDashboard(period, selected, errors=errors)
    # Generate the report
    result = CONTROLLERS[period]().generateReport(projectID, start, end)
    if not result["project"]:
        return displayDashboard(period, selected, errors={"projectID": "The selected project was not found."})
    if not result["report"]:                                            # no records in the period
        return displayDashboard(period, selected, message=NO_DATA_MESSAGES[period])
    return displayDashboard(period, selected, report=result["report"])


@project_reports.route("/platform/reports/<any(daily, weekly, monthly):period>", methods=["GET", "POST"])
def reportDashboard(period: str) -> str:
    if request.method == "POST":
        # Platform Administrator chose a project and period and clicked Generate Report
        return submitReport(period)
    # Platform Administrator opens Project Reports
    return displayDashboard(period)


@project_reports.route("/platform/reports/<any(daily, weekly, monthly):period>/download/<reportID>")
def downloadReport(period: str, reportID: str):
    csvContent = CONTROLLERS[period]().getReportCSV(reportID)
    if not csvContent:
        flash("This report is no longer available. Generate it again.", "err")
        return redirect(url_for("project_reports.reportDashboard", period=period))
    return send_file(BytesIO(csvContent.encode("utf-8-sig")), mimetype="text/csv", as_attachment=True,
                     download_name=f"{period}-project-report-{reportID}.csv")

"""Boundary helpers shared by the portfolio pages (#52-#61).
"kind" in a URL is "current" or "past"; the pages pick the matching controller with it."""
from datetime import date, datetime

from flask import request

KIND_LABELS = {"current": "Current Project", "past": "Past Project"}
MAX_LENGTHS = {"title": 100, "description": 1000, "designs": 500, "materials": 500, "category": 50}
REQUIRED_MESSAGES = {
    "title": "Please enter a project title.",
    "description": "Please enter a project description.",
    "designs": "Please describe the designs.",
    "materials": "Please list the materials.",
}


def readPortfolioForm(kind: str) -> dict:
    """The typed values, trimmed. A completion date is only read for past projects."""
    form = {f: request.form.get(f, "").strip() for f in MAX_LENGTHS}
    form["completionDate"] = request.form.get("completionDate", "").strip() if kind == "past" else ""
    return form


def validateForm(form: dict, kind: str) -> dict:
    """Boundary input check for #52 / #57 (5a) and #54 / #59 (6a): required fields, lengths and,
    for past projects, a real completion date that is not in the future.
    Returns fieldErrors; empty dict = all valid."""
    fieldErrors = {f: msg for f, msg in REQUIRED_MESSAGES.items() if not form[f]}
    for f, limit in MAX_LENGTHS.items():
        if len(form[f]) > limit:
            fieldErrors[f] = f"Must be {limit} characters or fewer."
    if kind == "past":
        if not form["completionDate"]:
            fieldErrors["completionDate"] = "Please enter the completion date."
        else:
            try:
                completed = datetime.strptime(form["completionDate"], "%Y-%m-%d").date()
                if completed > date.today():
                    fieldErrors["completionDate"] = "The completion date cannot be in the future."
            except ValueError:
                fieldErrors["completionDate"] = "Please enter a valid date."
    return fieldErrors

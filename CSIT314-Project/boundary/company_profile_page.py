"""«Boundary» CompanyProfilePage — #09 Create, #10 View, #11 Update company profile
(validateContactFields() is shared with #12 Manage contact information)
(no class: company_view.html, company_form.html + route functions).
Precondition (logged-in Interior Designer) is enforced by requireDesigner() in app.py.
Fields and validation rules follow Dominic's design (app.py.backup)."""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from control import (CreateCompanyProfileController, ViewCompanyProfileController,
                     UpdateCompanyProfileController)
from boundary.profiles import validateEmail

company_profile = Blueprint("company_profile", __name__)

COMPANY_PROFILE_FIELDS = ("companyName", "description", "businessEmail",
                          "businessPhone", "businessAddress", "website")

REQUIRED_MESSAGES = {
    "companyName": "Please enter your company name.",
    "description": "Please enter a company description.",
}
CONTACT_REQUIRED_MESSAGES = {
    "businessEmail": "Please enter a business email.",
    "businessPhone": "Please enter a business phone number.",
    "businessAddress": "Please enter a business address.",
}

MAX_LENGTHS = {"companyName": 100, "description": 1000}
CONTACT_MAX_LENGTHS = {"businessEmail": 100, "businessPhone": 20, "businessAddress": 200, "website": 200}

SAVE_FAILED = "Unable to save company profile. Please try again."


# ---- shared Boundary helpers -------------------------------------------------
def readCompanyProfileForm() -> dict:
    return {f: request.form.get(f, "").strip() for f in COMPANY_PROFILE_FIELDS}


def validateCompanyProfileForm(formData: dict) -> dict:
    """Boundary input check (#09 alt 2a / #11 alt 3a): every field except website is required,
    email / phone / website must be in a valid format.
    Returns fieldErrors, e.g. {"companyName": "..."}; empty dict = all valid."""
    fieldErrors = {f: msg for f, msg in REQUIRED_MESSAGES.items() if not formData[f]}
    for f, limit in MAX_LENGTHS.items():
        if len(formData[f]) > limit:
            fieldErrors[f] = f"Must be {limit} characters or fewer."
    fieldErrors.update(validateContactFields(formData))
    return fieldErrors


def validateContactFields(formData: dict) -> dict:
    """Boundary input check for the business contact fields, shared by #09 / #11 and #12:
    email, phone and address required, valid formats, length limits. Returns fieldErrors."""
    fieldErrors = {f: msg for f, msg in CONTACT_REQUIRED_MESSAGES.items() if not formData[f]}
    for f, limit in CONTACT_MAX_LENGTHS.items():
        if len(formData[f]) > limit:
            fieldErrors[f] = f"Must be {limit} characters or fewer."

    email = formData["businessEmail"]
    if "businessEmail" not in fieldErrors and validateEmail(email):
        fieldErrors["businessEmail"] = "Please enter a valid email address."

    phone = formData["businessPhone"].replace(" ", "").replace("-", "").lstrip("+")
    if "businessPhone" not in fieldErrors and (not phone.isdigit() or len(phone) < 8):
        fieldErrors["businessPhone"] = "Please enter a valid phone number (at least 8 digits)."

    website = formData["website"]
    if website and "website" not in fieldErrors and not website.startswith(("http://", "https://")):
        fieldErrors["website"] = "Website must start with http:// or https://"
    return fieldErrors


def displayCompanyProfileForm(mode: str, formData: dict, fieldErrors: dict = None,
                              error: str = None) -> str:
    return render_template("company_form.html", mode=mode, data=formData,
                           fieldErrors=fieldErrors or {}, error=error, active="company")


# ---- #10 View company profile ------------------------------------------------
def displayCompanyProfile(companyProfile: dict) -> str:                 # step 3
    return render_template("company_view.html", companyProfile=companyProfile, active="company")


def displayProfileNotCreated() -> str:                                  # alt 2a
    return render_template("company_view.html", companyProfile={}, active="company")


@company_profile.route("/designer/company")
def viewCompanyProfilePage() -> str:
    # Step 1: ID selects "View Company Profile"
    # Step 2: retrieve the company profile
    companyProfile = ViewCompanyProfileController().getCompanyProfile(session["u"])
    if not companyProfile:
        return displayProfileNotCreated()                   # [not created] 2a
    return displayCompanyProfile(companyProfile)            # [else] step 3


# ---- #09 Create company profile ----------------------------------------------
@company_profile.route("/designer/company/create", methods=["GET", "POST"])
def createCompanyProfilePage():
    u = session["u"]
    controller = CreateCompanyProfileController()
    if controller.checkProfileExists(u):                    # one profile per ID
        flash("You already have a company profile. Use Update to change it.", "info")
        return redirect(url_for("company_profile.viewCompanyProfilePage"))

    # Step 1: ID selects "Create Company Profile", system shows the form
    if request.method == "GET":
        return displayCompanyProfileForm("create", {})

    # Step 2: ID enters the company information and submits
    formData = readCompanyProfileForm()

    # Step 3: system validates the information...
    fieldErrors = validateCompanyProfileForm(formData)
    if fieldErrors:
        return displayCompanyProfileForm("create", formData, fieldErrors)      # alt 2a

    # ...and saves the company profile
    controller.createCompanyProfile(u, formData)
    flash("Company profile created successfully.", "ok")
    return redirect(url_for("company_profile.viewCompanyProfilePage"))


# ---- #11 Update company information ------------------------------------------
@company_profile.route("/designer/company/update", methods=["GET", "POST"])
def updateCompanyProfilePage():
    u = session["u"]
    controller = UpdateCompanyProfileController()
    companyProfile = controller.getCompanyProfile(u)
    if not companyProfile:                                  # precondition: profile exists
        flash("Company profile has not been created.", "err")
        return redirect(url_for("company_profile.viewCompanyProfilePage"))

    # Steps 1-2: ID selects "Update Company Information", system shows the current details
    if request.method == "GET":
        return displayCompanyProfileForm("update", companyProfile)

    # Step 3: ID submits the changes, system validates and saves
    formData = readCompanyProfileForm()
    fieldErrors = validateCompanyProfileForm(formData)
    if fieldErrors:
        return displayCompanyProfileForm("update", formData, fieldErrors)      # alt 3a

    profileUpdated = controller.updateCompanyProfile(u, formData)
    if not profileUpdated:
        return displayCompanyProfileForm("update", formData, error=SAVE_FAILED)
    flash("Company information updated successfully.", "ok")
    return redirect(url_for("company_profile.viewCompanyProfilePage"))

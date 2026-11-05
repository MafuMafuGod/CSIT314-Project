"""«Boundary» ManageContactInfoPage — #12 Manage company contact information
(no class: manage_contact_info.html + route functions).
Precondition (logged-in Interior Designer) is enforced by requireDesigner() in app.py.
The business email / phone / address / website checks are shared with #09 / #11."""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from control import ManageContactInfoController
from boundary.company_profile_page import validateContactFields

manage_contact_info = Blueprint("manage_contact_info", __name__)

CONTACT_FIELDS = ("businessEmail", "businessPhone", "businessAddress", "website",
                  "instagram", "facebook", "linkedin")
SOCIAL_MAX_LENGTH = 100


def readContactForm() -> dict:
    return {f: request.form.get(f, "").strip() for f in CONTACT_FIELDS}


def validateContactInfo(contactData: dict) -> dict:                     # step 3 (alt)
    """Boundary input check. Returns fieldErrors; empty dict = all valid."""
    fieldErrors = validateContactFields(contactData)
    for f in ("instagram", "facebook", "linkedin"):
        if len(contactData[f]) > SOCIAL_MAX_LENGTH:
            fieldErrors[f] = f"Must be {SOCIAL_MAX_LENGTH} characters or fewer."
    return fieldErrors


def displayContactForm(profile: dict, fieldErrors: dict = None, error: str = None) -> str:   # step 2
    return render_template("manage_contact_info.html", profile=profile, fieldErrors=fieldErrors or {},
                           error=error, active="company")


def displayProfileNotCreated() -> str:                                  # precondition failed
    flash("Create your company profile before managing contact information.", "err")
    return redirect(url_for("company_profile.viewCompanyProfilePage"))


def displaySuccess() -> str:                                            # step 4
    flash("Contact information updated successfully.", "ok")
    return redirect(url_for("manage_contact_info.manageContactInfo"))


@manage_contact_info.route("/designer/contact-info", methods=["GET"])
def manageContactInfo() -> str:
    # Step 1: ID opens Contact Details; the existing contact information is shown
    profile = ManageContactInfoController().getCompanyProfile(session["u"])
    if not profile:
        return displayProfileNotCreated()
    return displayContactForm(profile)


@manage_contact_info.route("/designer/contact-info/save", methods=["POST"])
def saveContactInfo() -> str:
    # Step 2: ID edits the contact fields and clicks Save Changes
    controller = ManageContactInfoController()
    profile = controller.getCompanyProfile(session["u"])
    if not profile:
        return displayProfileNotCreated()
    contactData = readContactForm()

    # Step 3: Boundary validates the contact fields...
    fieldErrors = validateContactInfo(contactData)
    if fieldErrors:
        return displayContactForm({**profile, **contactData}, fieldErrors)

    # ...and the contact information is saved
    contactUpdated = controller.updateContactInfo(session["u"], contactData)
    if not contactUpdated:
        return displayContactForm({**profile, **contactData},
                                  error="Unable to update contact information. Please try again.")
    return displaySuccess()

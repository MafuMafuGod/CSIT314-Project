"""«Control» ManageContactInfoController — #12 Manage company contact information."""
from entity import CompanyProfile


class ManageContactInfoController:
    """Gets the ID's company profile and saves the contact fields. Input validation is done
    by the Boundary."""

    def getCompanyProfile(self, designerU: str) -> dict:
        """Step 1: returns companyProfile ({} = not created yet)."""
        return CompanyProfile.getProfile(designerU)

    def updateContactInfo(self, designerU: str, contactData: dict) -> bool:
        """Step 3: returns contactUpdated from the Entity."""
        return CompanyProfile.updateContactInfo(
            designerU, contactData["businessEmail"], contactData["businessPhone"],
            contactData["businessAddress"], contactData["website"], contactData["instagram"],
            contactData["facebook"], contactData["linkedin"])

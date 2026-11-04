"""«Control» UpdateCompanyProfileController — #11 Update company information."""
from entity import CompanyProfile


class UpdateCompanyProfileController:
    """Gets the current company information and saves the changes. Input validation is done by the Boundary."""

    def getCompanyProfile(self, u: str) -> dict:
        """Step 2: returns companyProfile, to pre-fill the form ({} if not created)."""
        return CompanyProfile.getProfile(u)

    def updateCompanyProfile(self, u: str, formData: dict) -> bool:
        """Step 3: returns profileUpdated from the Entity."""
        return CompanyProfile.updateProfile(
            u, formData["companyName"], formData["description"], formData["businessEmail"],
            formData["businessPhone"], formData["businessAddress"], formData["website"])

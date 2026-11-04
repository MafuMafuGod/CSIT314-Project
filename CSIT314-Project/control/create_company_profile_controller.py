"""«Control» CreateCompanyProfileController — #09 Create company profile."""
from entity import CompanyProfile


class CreateCompanyProfileController:
    """Checks stored data and creates the company profile. Input validation is done by the Boundary."""

    def checkProfileExists(self, u: str) -> bool:
        """Precondition: returns profileExists from the Entity."""
        return CompanyProfile.profileExists(u)

    def createCompanyProfile(self, u: str, formData: dict) -> bool:
        """Step 3: returns profileCreated from the Entity."""
        return CompanyProfile.createProfile(
            u, formData["companyName"], formData["description"], formData["businessEmail"],
            formData["businessPhone"], formData["businessAddress"], formData["website"])

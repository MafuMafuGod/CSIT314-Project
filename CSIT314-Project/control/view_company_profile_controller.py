"""«Control» ViewCompanyProfileController — #10 View company profile."""
from entity import CompanyProfile


class ViewCompanyProfileController:
    """Gets the ID's company profile from the Entity."""

    def getCompanyProfile(self, u: str) -> dict:
        """Step 2: returns companyProfile ({} if not created)."""
        return CompanyProfile.getProfile(u)

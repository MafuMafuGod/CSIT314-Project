"""«Control» SearchCompanyProfilesController — #13 Search company profiles."""
from entity import CompanyProfile


class SearchCompanyProfilesController:
    """Gets the company profiles matching the keyword from the Entity."""

    def searchCompanyProfiles(self, keyword: str) -> list:
        """Returns matchingProfiles ([] = no matching company profiles)."""
        return CompanyProfile.searchProfiles(keyword)

"""«Control» SearchShortlistController — #35 Search Shortlist."""
from entity import InteriorDesignProject, Shortlist


class SearchShortlistController:
    """Gets the Customer's saved IDPs and filters them by keyword."""

    def getSavedIDPs(self, customerU: str) -> list:
        """Step 5: returns savedIDPs ([] = Shortlist is empty, 5a)."""
        return InteriorDesignProject.getIDPCards(Shortlist.getSavedIDPIDs(customerU))

    def searchShortlist(self, customerU: str, keyword: str) -> list:
        """Step 6: returns matchingIDPs ([] = no matching saved IDPs, 6a)."""
        return InteriorDesignProject.getIDPCards(Shortlist.getSavedIDPIDs(customerU), keyword)

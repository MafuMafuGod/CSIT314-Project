"""«Control» SearchIDPController — #32 Search IDPs."""
from entity import InteriorDesignProject


class SearchIDPController:
    """Gets the category list and the matching IDPs from the Entity."""

    def getCategories(self) -> list:
        """Step 2: returns categories for the search form."""
        return InteriorDesignProject.getCategories()

    def searchIDPs(self, keyword: str, category: str) -> list:
        """Step 6: returns idpList (empty = no matching IDPs)."""
        return InteriorDesignProject.findMatchingIDPs(keyword, category)

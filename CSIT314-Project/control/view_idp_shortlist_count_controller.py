"""«Control» ViewIDPShortlistCountController — #41 (Matthew)."""
from entity import InteriorDesignProject


class ViewIDPShortlistCountController:
    """#41: gets the ID's IDP shortlist counts from the Entity."""

    def getShortlistCounts(self, u: str) -> list:
        """Step 2: returns idpShortlistCounts."""
        return InteriorDesignProject.getShortlistCounts(u)

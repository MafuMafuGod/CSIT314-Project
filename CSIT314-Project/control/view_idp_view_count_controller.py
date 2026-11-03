"""«Control» ViewIDPViewCountController — #40 (Matthew)."""
from entity import InteriorDesignProject


class ViewIDPViewCountController:
    """#40: gets the ID's IDP view counts from the Entity."""

    def getViewCounts(self, u: str) -> list:
        """Step 2: returns idpViewCounts."""
        return InteriorDesignProject.getViewCounts(u)

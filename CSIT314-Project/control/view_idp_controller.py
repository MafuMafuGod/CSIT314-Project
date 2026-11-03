"""«Control» ViewIDPController — #33 View IDP Details."""
from entity import InteriorDesignProject


class ViewIDPController:
    """Gets the selected IDP's details from the Entity and records the view for #40."""

    def viewIDPDetails(self, idpID: int) -> dict:
        """Step 3: returns idp ({} = not found, 3a).
        A successful view is counted, so the designer's view count (#40) stays correct."""
        idp = InteriorDesignProject.findIDPByID(idpID)
        if idp:
            InteriorDesignProject.incrementViewCount(idpID)
        return idp

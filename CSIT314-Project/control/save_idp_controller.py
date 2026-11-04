"""«Control» SaveIDPController — #34 Save IDP to Shortlist (favourite list)."""
from entity import InteriorDesignProject, Shortlist


class SaveIDPController:
    """Checks for a duplicate, saves the IDP and records the save for #41."""

    def isIDPSaved(self, customerU: str, idpID: int) -> bool:
        """Step 3: returns alreadySaved from the Entity."""
        return Shortlist.isSaved(customerU, idpID)

    def saveIDP(self, customerU: str, idpID: int) -> bool:
        """Step 4: returns saved (False = the IDP no longer exists, 4a).
        A new save is counted, so the designer's shortlist count (#41) stays correct."""
        if not InteriorDesignProject.findIDPByID(idpID):
            return False
        Shortlist.saveIDP(customerU, idpID)
        InteriorDesignProject.incrementShortlistCount(idpID)
        return True

    def getIDPDetails(self, idpID: int) -> dict:
        """Step 5: the IDP to show again with the confirmation ({} = not found)."""
        return InteriorDesignProject.findIDPByID(idpID)

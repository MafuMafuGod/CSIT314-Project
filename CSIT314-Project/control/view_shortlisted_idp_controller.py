"""«Control» 
ViewShortlistedIDPController — #36 View Shortlisted IDP"""
from entity import InteriorDesignProject, Shortlist


class ViewShortlistedIDPController:
    """Checks the IDP is in the Customer's Shortlist and gets its details"""

    def isInShortlist(self, customerU: str, idpID: int) -> bool:
        """Step 4: returns inShortlist ([False] = 4a)"""
        # True if this Customer saved this IDP
        return Shortlist.isSaved(customerU, idpID)

    def getIDPDetails(self, idpID: int) -> dict:
        """Step 5: returns idp ({} = no longer available, 5a)"""
        return InteriorDesignProject.findIDPByID(idpID)

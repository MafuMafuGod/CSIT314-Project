"""«Entity» 
Shortlist — each Customer's favourite list of IDPs
Used by #34 Save IDP to Shortlist, #35 Search Shortlist, #36 View Shortlisted IDP."""
from datetime import date


class Shortlist:
    """One saved IDP in one Customer's Shortlist."""

    _entries = []                       # stand-in for the database table

    def __init__(self, customerU: str, idpID: int, savedDate: str = "") -> None:
        self._customerU = customerU      # the Customer's username (email)
        self._idpID = idpID
        self._savedDate = savedDate or date.today().isoformat()

    # ---- #34 Save IDP to Shortlist ------------------------------------------
    # @classmethod = the method is called on the class itself, e.g. Shortlist.isSaved(...)
    @classmethod
    def isSaved(cls, customerU: str, idpID: int) -> bool:
        """#34 step 3 / #36 step 4: is this IDP already in the Customer's Shortlist?"""
        # True if at least one saved row has this Customer and this IDP
        return any(e._customerU == customerU and e._idpID == idpID for e in cls._entries)

    @classmethod
    def saveIDP(cls, customerU: str, idpID: int) -> bool:
        """#34 step 4: add the IDP to the Customer's Shortlist."""
        # add one new row to the table
        cls._entries.append(Shortlist(customerU, idpID))
        return True

    # ---- #35 Search Shortlist -----------------------------------------------
    @classmethod
    def getSavedIDPIDs(cls, customerU: str) -> list:
        """#35 step 5: the IDs of the IDPs the Customer has saved, newest first."""
        # only this Customer's rows, newest first (reversed)
        return [e._idpID for e in reversed(cls._entries) if e._customerU == customerU]


# Sample data: the demo Customer starts with two saved IDPs
Shortlist._entries = [
    Shortlist("customer@4reno.com", 2, "2026-10-20"),
    Shortlist("customer@4reno.com", 4, "2026-10-22"),
]

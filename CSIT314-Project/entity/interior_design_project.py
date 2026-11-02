"""«Entity» InteriorDesignProject — used by #40, #41 (Matthew) and portfolio #52-#56.

Tracking hooks for other use cases (call these through a Controller, don't edit the counts directly):
  #33 View IDP details       -> InteriorDesignProject.incrementViewCount(idpID)
  #34 Save IDP to shortlist  -> InteriorDesignProject.incrementShortlistCount(idpID)
"""
from typing import Optional


class InteriorDesignProject:
    """An Interior Design Project (IDP) owned by one Interior Designer."""

    _idps = []                          # stand-in for the database table

    def __init__(self, idpID: int, designerU: str, title: str, createdDate: str,
                 viewCount: int = 0, shortlistCount: int = 0) -> None:
        self._idpID = idpID
        self._designerU = designerU      # the ID's username (email)
        self._title = title              # project name
        self._createdDate = createdDate  # "YYYY-MM-DD"
        self._viewCount = viewCount
        self._shortlistCount = shortlistCount

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findIDP(cls, idpID: int) -> Optional["InteriorDesignProject"]:
        for idp in cls._idps:
            if idp._idpID == idpID:
                return idp
        return None

    @classmethod
    def _getIDPsByDesigner(cls, designerU: str) -> list:
        return [idp for idp in cls._idps if idp._designerU == designerU]

    @classmethod
    def _getCounts(cls, designerU: str, field: str) -> list:
        """Shared by #40 and #41: the ID's IDPs with one count field, highest first."""
        rows = [{"idpID": idp._idpID, "title": idp._title,
                 "createdDate": idp._createdDate, field: getattr(idp, "_" + field)}
                for idp in cls._getIDPsByDesigner(designerU)]
        return sorted(rows, key=lambda r: r[field], reverse=True)

    # ---- #40 step 2: the ID's IDPs with their view counts --------------------
    @classmethod
    def getViewCounts(cls, designerU: str) -> list:
        """Returns idpViewCounts, most-viewed first. [] if the ID has no IDP."""
        return cls._getCounts(designerU, "viewCount")

    # ---- #41 step 2: the ID's IDPs with their shortlist counts ---------------
    @classmethod
    def getShortlistCounts(cls, designerU: str) -> list:
        """Returns idpShortlistCounts, most-shortlisted first. [] if the ID has no IDP."""
        return cls._getCounts(designerU, "shortlistCount")

    # ---- tracking: called by #33 and #34 ---------------------------------------
    @classmethod
    def incrementViewCount(cls, idpID: int) -> bool:
        """A customer viewed the IDP's details (#33)."""
        idp = cls._findIDP(idpID)
        if idp is None:
            return False
        idp._viewCount += 1
        return True

    @classmethod
    def incrementShortlistCount(cls, idpID: int) -> bool:
        """A customer saved the IDP to their shortlist (#34). Call only when
        the save is new, so a duplicate save (#34 alt 3a) is not counted."""
        idp = cls._findIDP(idpID)
        if idp is None:
            return False
        idp._shortlistCount += 1
        return True


# Sample data (replace with the shared 100-record test data script later)
InteriorDesignProject._idps = [
    InteriorDesignProject(1, "designer@4reno.com", "Tampines HDB Scandinavian Makeover", "2026-08-14", 342, 41),
    InteriorDesignProject(2, "designer@4reno.com", "Punggol Waterway Condo Kitchen", "2026-09-02", 518, 77),
    InteriorDesignProject(3, "designer@4reno.com", "Bishan Landed Home Revamp", "2026-09-21", 129, 12),
    InteriorDesignProject(4, "designer@4reno.com", "Sengkang BTO Minimalist Living Room", "2026-10-08", 87, 15),
    InteriorDesignProject(5, "designer@4reno.com", "Clementi Resale Japandi Bedroom", "2026-10-19", 23, 2),
]

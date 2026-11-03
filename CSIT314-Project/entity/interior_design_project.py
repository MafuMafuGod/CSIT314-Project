"""«Entity» InteriorDesignProject — used by #32 Search IDPs, #40, #41 (Matthew) and portfolio #52-#56.

Tracking hooks for other use cases (call these through a Controller, don't edit the counts directly):
  #33 View IDP details       -> InteriorDesignProject.incrementViewCount(idpID)
  #34 Save IDP to shortlist  -> InteriorDesignProject.incrementShortlistCount(idpID)
"""
from typing import Optional


class InteriorDesignProject:
    """An Interior Design Project (IDP) owned by one Interior Designer."""

    _idps = []                          # stand-in for the database table

    def __init__(self, idpID: int, designerU: str, title: str, createdDate: str,
                 viewCount: int = 0, shortlistCount: int = 0,
                 description: str = "", category: str = "", imageURL: str = "") -> None:
        self._idpID = idpID
        self._designerU = designerU      # the ID's username (email)
        self._title = title              # project name
        self._createdDate = createdDate  # "YYYY-MM-DD"
        self._viewCount = viewCount
        self._shortlistCount = shortlistCount
        self._description = description  # shown on the details page, searched by keyword
        self._category = category        # e.g. "Living Room", "Kitchen"
        self._imageURL = imageURL        # "" = show the image placeholder

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

    def _toCard(self) -> dict:
        """Fields needed by a search result card."""
        return {"idpID": self._idpID, "title": self._title, "category": self._category,
                "imageURL": self._imageURL}

    # ---- #32 Search IDPs -------------------------------------------------------
    @classmethod
    def getCategories(cls) -> list:
        """#32 step 2: every category in use, A-Z, for the search form."""
        return sorted({idp._category for idp in cls._idps if idp._category})

    @classmethod
    def findMatchingIDPs(cls, keyword: str, category: str) -> list:
        """#32 step 6: IDPs whose title or description contains the keyword
        (case-insensitive) and whose category matches. An empty keyword or
        category means "any". Returns [] if nothing matches (6a)."""
        keyword = keyword.lower()
        return [idp._toCard() for idp in cls._idps
                if (not keyword or keyword in idp._title.lower() or keyword in idp._description.lower())
                and (not category or idp._category == category)]

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
    InteriorDesignProject(1, "designer@4reno.com", "Tampines HDB Scandinavian Makeover", "2026-08-14", 342, 41,
                          "Light oak floors, white walls and simple furniture for a bright 4-room flat.", "Living Room"),
    InteriorDesignProject(2, "designer@4reno.com", "Punggol Waterway Condo Kitchen", "2026-09-02", 518, 77,
                          "Open kitchen with a quartz island, hidden storage and warm lighting.", "Kitchen"),
    InteriorDesignProject(3, "designer@4reno.com", "Bishan Landed Home Revamp", "2026-09-21", 129, 12,
                          "Whole-house renovation of a terrace home with an industrial loft feel.", "Whole House"),
    InteriorDesignProject(4, "designer@4reno.com", "Sengkang BTO Minimalist Living Room", "2026-10-08", 87, 15,
                          "Minimalist living room with built-in TV console and neutral tones.", "Living Room"),
    InteriorDesignProject(5, "designer@4reno.com", "Clementi Resale Japandi Bedroom", "2026-10-19", 23, 2,
                          "Japandi master bedroom with timber platform bed and soft linen textures.", "Bedroom"),
]

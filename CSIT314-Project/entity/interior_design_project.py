"""«Entity» InteriorDesignProject — used by #32 Search IDPs, #33 View IDP Details,
#34 / #35 / #36 Shortlist, #40, #41 (Matthew), #62-#64 reports, #65-#69 categories and the portfolio:
  current projects #52 Create, #53 View, #54 Update, #55 Delete, #56 Search
  past projects    #57 Create, #58 View, #59 Update, #60 Delete, #61 Search
"""


from datetime import date
from typing import Optional


class InteriorDesignProject:
    """An Interior Design Project (IDP) in one Interior Designer's portfolio."""

    _idps = []                          # stand-in for the database table

    def __init__(self, idpID: int, designerU: str, title: str, createdDate: str,
                 viewCount: int = 0, shortlistCount: int = 0,
                 description: str = "", category: str = "", imageURL: str = "",
                 designs: str = "", materials: str = "", status: str = "Current",
                 completionDate: str = "") -> None:
        self._idpID = idpID
        self._designerU = designerU      # the ID's username (email)
        self._title = title              # project name
        self._createdDate = createdDate  # "YYYY-MM-DD"
        self._viewCount = viewCount
        self._shortlistCount = shortlistCount
        self._description = description  # shown on the details page, searched by keyword
        self._category = category        # e.g. "Living Room", "Kitchen"
        self._imageURL = imageURL        # "" = show the image placeholder
        self._designs = designs          # design concept / style, e.g. "Japandi, open-plan"
        self._materials = materials      # e.g. "Oak veneer, quartz countertop"
        self._status = status            # "Current" or "Past"
        self._completionDate = completionDate   # "YYYY-MM-DD" for past projects, "" otherwise

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findIDP(cls, idpID: int) -> Optional["InteriorDesignProject"]:
        for idp in cls._idps:
            if idp._idpID == idpID:
                return idp
        return None

    @classmethod
    def _findOwnProject(cls, designerU: str, idpID: int, status: str) -> Optional["InteriorDesignProject"]:
        """A project in this ID's portfolio with this status (None = not theirs / not found)."""
        idp = cls._findIDP(idpID)
        if idp is None or idp._designerU != designerU or idp._status != status:
            return None
        return idp

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

    def _matches(self, keyword: str, category: str) -> bool:
        """Any text field contains the keyword (not case-sensitive) and the category matches.
        Empty keyword / category = "any". Shared by #32, #35, #56 and #61."""
        keyword = keyword.lower()
        text = " ".join((self._title, self._description, self._designs, self._materials,
                         self._category)).lower()
        return (not keyword or keyword in text) and (not category or self._category == category)

    def _toCard(self) -> dict:
        """Fields needed by a search result card."""
        return {"idpID": self._idpID, "title": self._title, "category": self._category,
                "imageURL": self._imageURL}

    def _toPortfolioDict(self) -> dict:
        """Everything the portfolio pages show (#53 / #58)."""
        return {"idpID": self._idpID, "title": self._title, "description": self._description,
                "designs": self._designs, "materials": self._materials, "category": self._category,
                "status": self._status, "createdDate": self._createdDate,
                "completionDate": self._completionDate}

    # ---- #32 Search IDPs -------------------------------------------------------
    @classmethod
    def getCategories(cls) -> list:
        """#32 step 2: every category in use, A-Z."""
        return sorted({idp._category for idp in cls._idps if idp._category})

    @classmethod
    def findMatchingIDPs(cls, keyword: str, category: str) -> list:
        """#32 step 6: IDPs matching the keyword and category. [] if nothing matches (6a)."""
        return [idp._toCard() for idp in cls._idps if idp._matches(keyword, category)]

    # ---- #35 Search Shortlist ------------------------------------------------
    @classmethod
    def getIDPCards(cls, idpIDs: list, keyword: str = "") -> list:
        """#35 steps 5-6: cards for the given IDPs (e.g. a Customer's Shortlist), keeping only
        those that match the keyword. IDPs that no longer exist are left out."""
        return [idp._toCard() for idp in cls._idps if idp._idpID in idpIDs and idp._matches(keyword, "")]

    # ---- #33 View IDP Details --------------------------------------------------
    @classmethod
    def findIDPByID(cls, idpID: int) -> dict:
        """#33 step 3: the selected IDP's details. {} if it does not exist (3a)."""
        idp = cls._findIDP(idpID)
        if idp is None:
            return {}
        return {"idpID": idp._idpID, "title": idp._title, "description": idp._description,
                "category": idp._category, "imageURL": idp._imageURL}

    # ---- #52 / #57 Create portfolio ------------------------------------------
    @classmethod
    def createProject(cls, designerU: str, title: str, description: str, designs: str,
                      materials: str, category: str, status: str, completionDate: str = "") -> bool:
        """#52 step 6 (status "Current") / #57 step 6 (status "Past"): save the new project."""
        newID = max((idp._idpID for idp in cls._idps), default=0) + 1
        cls._idps.append(InteriorDesignProject(
            newID, designerU, title, date.today().isoformat(), description=description,
            category=category, designs=designs, materials=materials, status=status,
            completionDate=completionDate))
        return True

    # ---- #53 / #58 View portfolio --------------------------------------------
    @classmethod
    def getProjectsByStatus(cls, designerU: str, status: str) -> list:
        """#53 step 1 / #58: the ID's current or past projects, newest first."""
        projects = [idp._toPortfolioDict() for idp in cls._getIDPsByDesigner(designerU)
                    if idp._status == status]
        return sorted(projects, key=lambda p: p["idpID"], reverse=True)

    @classmethod
    def getProject(cls, designerU: str, idpID: int, status: str) -> dict:
        """#53 step 3 / #54 step 2 / #58 step 2 / #59 step 2: one project's portfolio
        information. {} if it is not in this ID's portfolio (3a / 2a: information unavailable)."""
        idp = cls._findOwnProject(designerU, idpID, status)
        return idp._toPortfolioDict() if idp else {}

    # ---- #54 / #59 Update portfolio ------------------------------------------
    @classmethod
    def updateProject(cls, designerU: str, idpID: int, status: str, title: str, description: str,
                      designs: str, materials: str, category: str, completionDate: str = "") -> bool:
        """#54 step 7 / #59 step 7: save the changes. False if the project is gone (7a)."""
        idp = cls._findOwnProject(designerU, idpID, status)
        if idp is None:
            return False
        idp._title, idp._description = title, description
        idp._designs, idp._materials, idp._category = designs, materials, category
        idp._completionDate = completionDate
        return True

    # ---- #55 / #60 Delete portfolio ------------------------------------------
    @classmethod
    def deleteProject(cls, designerU: str, idpID: int, status: str) -> bool:
        """#55 step 4 / #60 step 4: remove the project. False if it is not there (4a)."""
        idp = cls._findOwnProject(designerU, idpID, status)
        if idp is None:
            return False
        cls._idps.remove(idp)
        return True

    # ---- #56 / #61 Search portfolio ------------------------------------------
    @classmethod
    def searchProjects(cls, designerU: str, status: str, keyword: str) -> list:
        """#56 step 3 / #61 step 3: the ID's current or past projects matching the keyword.
        [] if nothing matches (4a)."""
        projects = [idp._toPortfolioDict() for idp in cls._getIDPsByDesigner(designerU)
                    if idp._status == status and idp._matches(keyword, "")]
        return sorted(projects, key=lambda p: p["idpID"], reverse=True)

    # ---- #62 / #63 / #64 Project reports -----------------------------------
    def _toSummary(self) -> dict:
        return {"projectID": self._idpID, "name": self._title, "status": self._status,
                "category": self._category, "designerU": self._designerU}

    @classmethod
    def getProjectSummaries(cls) -> list:
        """Every project on the platform, A-Z (#62-#64 report form, #65 / #66 project choice)."""
        return sorted((idp._toSummary() for idp in cls._idps), key=lambda p: p["name"].casefold())

    @classmethod
    def getProjectSummary(cls, idpID: int) -> dict:
        """One project's summary ({} if it does not exist)."""
        idp = cls._findIDP(idpID)
        return idp._toSummary() if idp else {}

    # ---- #65 - #69 IDP categories ------------------------------------------
    @classmethod
    def getProjectsInCategory(cls, categoryName: str) -> list:
        """#67 / #68 / #69: the projects linked to a category, A-Z."""
        return [p for p in cls.getProjectSummaries() if p["category"].casefold() == categoryName.casefold()]

    @classmethod
    def setProjectCategory(cls, idpID: int, categoryName: str) -> bool:
        """#65 / #66: link a project to a category (or move it to another one)."""
        idp = cls._findIDP(idpID)
        if idp is None:
            return False
        idp._category = categoryName
        return True

    @classmethod
    def renameCategory(cls, oldName: str, newName: str) -> int:
        """#66: keep projects linked when their category is renamed. Returns how many moved."""
        moved = [idp for idp in cls._idps if idp._category.casefold() == oldName.casefold()]
        for idp in moved:
            idp._category = newName
        return len(moved)

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
                          "Light oak floors, white walls and simple furniture for a bright 4-room flat.", "Living Room",
                          designs="Scandinavian, open-plan living and dining",
                          materials="Light oak vinyl flooring, white laminate, linen curtains",
                          status="Past", completionDate="2026-08-10"),
    InteriorDesignProject(2, "designer@4reno.com", "Punggol Waterway Condo Kitchen", "2026-09-02", 518, 77,
                          "Open kitchen with a quartz island, hidden storage and warm lighting.", "Kitchen",
                          designs="Modern open kitchen with island seating",
                          materials="Quartz countertop, walnut veneer cabinets, brass fittings",
                          status="Past", completionDate="2026-08-28"),
    InteriorDesignProject(3, "designer@4reno.com", "Bishan Landed Home Revamp", "2026-09-21", 129, 12,
                          "Whole-house renovation of a terrace home with an industrial loft feel.", "Whole House",
                          designs="Industrial loft, exposed beams, double-volume living",
                          materials="Cement screed, black steel, reclaimed timber",
                          status="Past", completionDate="2026-09-15"),
    InteriorDesignProject(4, "designer@4reno.com", "Sengkang BTO Minimalist Living Room", "2026-10-08", 87, 15,
                          "Minimalist living room with built-in TV console and neutral tones.", "Living Room",
                          designs="Minimalist, hidden storage, neutral palette",
                          materials="Matte laminate, fluted glass, beige microcement"),
    InteriorDesignProject(5, "designer@4reno.com", "Clementi Resale Japandi Bedroom", "2026-10-19", 23, 2,
                          "Japandi master bedroom with timber platform bed and soft linen textures.", "Bedroom",
                          designs="Japandi, low platform bed, soft lighting",
                          materials="Ash timber, rattan, linen"),
]

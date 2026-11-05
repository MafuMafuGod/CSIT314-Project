"""«Entity» IDPCategory — the categories an IDP can belong to.
Used by #65 Create, #66 Update, #67 View, #68 Delete and #69 Search IDP categories, and by the
portfolio form (#52 / #54 / #57 / #59), where a designer picks one of these categories.
A project is linked to a category by the category name stored on InteriorDesignProject."""
from datetime import date
from typing import Optional


class IDPCategory:
    """One IDP category, e.g. "Kitchen"."""

    _categories = []                    # stand-in for the database table
    _nextID = 1

    def __init__(self, name: str, description: str = "", createdDate: str = "") -> None:
        self._categoryID = f"IDP-CAT-{IDPCategory._nextID:03d}"
        IDPCategory._nextID += 1
        self._name = name
        self._description = description
        self._createdDate = createdDate or date.today().isoformat()

    # ---- private helpers ---------------------------------------------------
    @classmethod
    def _findCategory(cls, categoryID: str) -> Optional["IDPCategory"]:
        for category in cls._categories:
            if category._categoryID == categoryID:
                return category
        return None

    def _toDict(self) -> dict:
        return {"categoryID": self._categoryID, "name": self._name,
                "description": self._description, "createdDate": self._createdDate}

    # ---- lists -----------------------------------------------------------------
    @classmethod
    def getCategoryNames(cls) -> list:
        """Category names A-Z, for the portfolio form's category choice."""
        return sorted((c._name for c in cls._categories), key=str.casefold)

    @classmethod
    def listCategories(cls) -> list:
        """#67 / #69: every category, A-Z."""
        return sorted((c._toDict() for c in cls._categories), key=lambda c: c["name"].casefold())

    # ---- #65 Create ----------------------------------------------------------
    @classmethod
    def nameExists(cls, name: str, excludeCategoryID: str = "") -> bool:
        """#65 / #66: is the name taken by another category? (not case-sensitive)"""
        name = name.casefold()
        return any(c._name.casefold() == name and c._categoryID != excludeCategoryID
                   for c in cls._categories)

    @classmethod
    def createCategory(cls, name: str, description: str) -> str:
        """#65: store the new category. Returns its categoryID."""
        category = IDPCategory(name, description)
        cls._categories.append(category)
        return category._categoryID

    # ---- #67 View ------------------------------------------------------------
    @classmethod
    def getCategory(cls, categoryID: str) -> dict:
        """#66 / #67 / #68: one category's details ({} if it does not exist)."""
        category = cls._findCategory(categoryID)
        return category._toDict() if category else {}

    # ---- #66 Update ----------------------------------------------------------
    @classmethod
    def updateCategory(cls, categoryID: str, name: str, description: str) -> bool:
        """#66: save the new name and description. False if the category is gone."""
        category = cls._findCategory(categoryID)
        if category is None:
            return False
        category._name, category._description = name, description
        return True

    # ---- #68 Delete ----------------------------------------------------------
    @classmethod
    def deleteCategory(cls, categoryID: str) -> bool:
        """#68: remove the category. False if it is not there."""
        category = cls._findCategory(categoryID)
        if category is None:
            return False
        cls._categories.remove(category)
        return True

    # ---- #69 Search ----------------------------------------------------------
    @classmethod
    def searchCategories(cls, keyword: str) -> list:
        """#69: categories whose name or description contains the keyword (not case-sensitive)."""
        keyword = keyword.casefold()
        return [c for c in cls.listCategories()
                if keyword in c["name"].casefold() or keyword in c["description"].casefold()]


# Sample data: the categories the sample IDPs already use, plus Study
IDPCategory._categories = [
    IDPCategory("Bedroom", "Master and children's bedrooms", "2026-10-01"),
    IDPCategory("Kitchen", "Kitchens, pantries and dining areas", "2026-10-01"),
    IDPCategory("Living Room", "Living and family rooms", "2026-10-01"),
    IDPCategory("Study", "Home offices and study rooms", "2026-10-01"),
    IDPCategory("Whole House", "Full-home renovations", "2026-10-01"),
]

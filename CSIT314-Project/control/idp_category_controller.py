"""«Control» IDP category controllers — one per use case, sharing IDPCategoryController:
  #65 CreateIDPCategoryController   #66 UpdateIDPCategoryController
  #67 ViewIDPCategoryController     #68 DeleteIDPCategoryController
  #69 SearchIDPCategoryController
The Control layer links the two Entities: IDPCategory holds the categories and
InteriorDesignProject holds which category each project is in."""
from abc import ABC

from entity import IDPCategory, InteriorDesignProject


class IDPCategoryController(ABC):
    """Shared lookups for every category page. Not used directly."""

    def _withProjects(self, category: dict) -> dict:
        projects = InteriorDesignProject.getProjectsInCategory(category["name"])
        return {**category, "projects": projects, "projectCount": len(projects)}

    def getCategoryList(self) -> list:
        """Every category with its linked projects."""
        return [self._withProjects(c) for c in IDPCategory.listCategories()]

    def getCategory(self, categoryID: str) -> dict:
        """One category with its linked projects ({} = not found)."""
        category = IDPCategory.getCategory(categoryID)
        return self._withProjects(category) if category else {}

    def getProjects(self) -> list:
        """Every project, for choosing which ones to link."""
        return InteriorDesignProject.getProjectSummaries()


class CreateIDPCategoryController(IDPCategoryController):
    """#65 Create an IDP category (and optionally link projects to it)."""

    def categoryExists(self, name: str) -> bool:
        """Returns nameTaken from the Entity."""
        return IDPCategory.nameExists(name)

    def createCategory(self, name: str, description: str, projectIDs: list) -> str:
        """Returns the new categoryID; the chosen projects are linked to it."""
        categoryID = IDPCategory.createCategory(name, description)
        for projectID in projectIDs:
            InteriorDesignProject.setProjectCategory(projectID, name)
        return categoryID


class UpdateIDPCategoryController(IDPCategoryController):
    """#66 Update an IDP category's details or which projects are in it."""

    def categoryExists(self, name: str, categoryID: str) -> bool:
        """Is the name taken by another category? Returns nameTaken."""
        return IDPCategory.nameExists(name, categoryID)

    def updateCategory(self, categoryID: str, name: str, description: str) -> bool:
        """Returns updated. Projects stay linked when the category is renamed."""
        oldName = IDPCategory.getCategory(categoryID)["name"]
        updated = IDPCategory.updateCategory(categoryID, name, description)
        InteriorDesignProject.renameCategory(oldName, name)
        return updated

    def assignProject(self, categoryID: str, projectID: int) -> bool:
        """Link a project to this category (moving it from its old one). Returns assigned."""
        return InteriorDesignProject.setProjectCategory(projectID, IDPCategory.getCategory(categoryID)["name"])


class ViewIDPCategoryController(IDPCategoryController):
    """#67 View an IDP category and its projects (uses the shared lookups)."""


class DeleteIDPCategoryController(IDPCategoryController):
    """#68 Delete an IDP category that has no projects."""

    def deleteCategory(self, categoryID: str) -> bool:
        """Returns deleted from the Entity."""
        return IDPCategory.deleteCategory(categoryID)


class SearchIDPCategoryController(IDPCategoryController):
    """#69 Search IDP categories, then projects inside one category."""

    def searchCategories(self, keyword: str) -> list:
        """Returns matchingCategories with their projects."""
        return [self._withProjects(c) for c in IDPCategory.searchCategories(keyword)]

    def searchProjectsInCategory(self, categoryID: str, keyword: str) -> list:
        """Returns the category's projects whose name contains the keyword."""
        keyword = keyword.casefold()
        return [p for p in self.getCategory(categoryID).get("projects", []) if keyword in p["name"].casefold()]

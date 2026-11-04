"""«Control» UpdateCurrentProjectController (#54) and UpdatePastProjectController (#59)."""
from entity import InteriorDesignProject
from control.portfolio_project_controller import PortfolioProjectController


class UpdatePortfolioProjectController(PortfolioProjectController):
    """Shared by #54 and #59. Each subclass sets STATUS."""

    def getProject(self, designerU: str, idpID: int) -> dict:
        """Step 2: returns the existing portfolio information ({} = not found)."""
        return InteriorDesignProject.getProject(designerU, idpID, self.STATUS)

    def updateProject(self, designerU: str, idpID: int, title: str, description: str, designs: str,
                      materials: str, category: str, completionDate: str = "") -> bool:
        """Step 7: returns updated (False = save failed, 7a)."""
        return InteriorDesignProject.updateProject(designerU, idpID, self.STATUS, title, description,
                                                   designs, materials, category, completionDate)


class UpdateCurrentProjectController(UpdatePortfolioProjectController):
    """#54 Update portfolio of a current project."""
    STATUS = "Current"


class UpdatePastProjectController(UpdatePortfolioProjectController):
    """#59 Update portfolio of a past project."""
    STATUS = "Past"

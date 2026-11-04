"""«Control» CreateCurrentProjectController (#52) and CreatePastProjectController (#57).
Both create a portfolio project; they only differ in the status they save (inheritance)."""
from entity import InteriorDesignProject
from control.portfolio_project_controller import PortfolioProjectController


class CreatePortfolioProjectController(PortfolioProjectController):
    """Shared by #52 and #57. Each subclass sets STATUS."""

    def createProject(self, designerU: str, title: str, description: str, designs: str,
                      materials: str, category: str, completionDate: str = "") -> bool:
        """Step 6: returns created from the Entity."""
        return InteriorDesignProject.createProject(designerU, title, description, designs,
                                                   materials, category, self.STATUS, completionDate)


class CreateCurrentProjectController(CreatePortfolioProjectController):
    """#52 Create portfolio for a current project (saved with status "Current")."""
    STATUS = "Current"


class CreatePastProjectController(CreatePortfolioProjectController):
    """#57 Create portfolio for a past project (saved with status "Past")."""
    STATUS = "Past"

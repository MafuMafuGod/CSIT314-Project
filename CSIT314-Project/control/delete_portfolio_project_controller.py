"""«Control» DeleteCurrentProjectController (#55) and DeletePastProjectController (#60)."""
from entity import InteriorDesignProject
from control.portfolio_project_controller import PortfolioProjectController


class DeletePortfolioProjectController(PortfolioProjectController):
    """Shared by #55 and #60. Each subclass sets STATUS."""

    def deleteProject(self, designerU: str, idpID: int) -> bool:
        """Step 4: returns deleted (False = deletion failed, 4a)."""
        return InteriorDesignProject.deleteProject(designerU, idpID, self.STATUS)


class DeleteCurrentProjectController(DeletePortfolioProjectController):
    """#55 Delete portfolio of a current project."""
    STATUS = "Current"


class DeletePastProjectController(DeletePortfolioProjectController):
    """#60 Delete portfolio of a past project."""
    STATUS = "Past"

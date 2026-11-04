"""«Control» ViewCurrentProjectController (#53) and ViewPastProjectController (#58)."""
from entity import InteriorDesignProject
from control.portfolio_project_controller import PortfolioProjectController


class ViewPortfolioProjectController(PortfolioProjectController):
    """Shared by #53 and #58. Each subclass sets STATUS."""

    def getProjectList(self, designerU: str) -> list:
        """#53 step 1 / #58 step 1: returns the ID's projects with this status."""
        return InteriorDesignProject.getProjectsByStatus(designerU, self.STATUS)

    def getProject(self, designerU: str, idpID: int) -> dict:
        """#53 step 3 / #58 step 2: returns project ({} = information unavailable)."""
        return InteriorDesignProject.getProject(designerU, idpID, self.STATUS)


class ViewCurrentProjectController(ViewPortfolioProjectController):
    """#53 View portfolio of a current project."""
    STATUS = "Current"


class ViewPastProjectController(ViewPortfolioProjectController):
    """#58 View portfolio of a past project."""
    STATUS = "Past"

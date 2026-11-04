"""«Control» SearchCurrentProjectController (#56) and SearchPastProjectController (#61)."""
from entity import InteriorDesignProject
from control.portfolio_project_controller import PortfolioProjectController


class SearchPortfolioProjectController(PortfolioProjectController):
    """Shared by #56 and #61. Each subclass sets STATUS."""

    def searchProjects(self, designerU: str, keyword: str) -> list:
        """Step 3: returns matchingProjects ([] = no matching results, 4a)."""
        return InteriorDesignProject.searchProjects(designerU, self.STATUS, keyword)


class SearchCurrentProjectController(SearchPortfolioProjectController):
    """#56 Search portfolio of current projects."""
    STATUS = "Current"


class SearchPastProjectController(SearchPortfolioProjectController):
    """#61 Search portfolio of past projects."""
    STATUS = "Past"

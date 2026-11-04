"""«Control» PortfolioProjectController — the abstract parent of every portfolio controller
(#52-#61). A subclass only sets STATUS ("Current" or "Past"), so one class per use case
shares the same code (inheritance + polymorphism)."""
from abc import ABC

from entity import InteriorDesignProject


class PortfolioProjectController(ABC):
    """Not used directly: each use case has its own subclass that sets STATUS."""

    STATUS = ""

    def getCategories(self) -> list:
        """Existing categories, suggested in the create / edit form."""
        return InteriorDesignProject.getCategories()

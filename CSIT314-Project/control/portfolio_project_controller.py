"""«Control» PortfolioProjectController — the abstract parent of every portfolio controller
(#52-#61). A subclass only sets STATUS ("Current" or "Past"), so one class per use case
shares the same code (inheritance + polymorphism)."""
from abc import ABC

from entity import IDPCategory


class PortfolioProjectController(ABC):
    """Not used directly: each use case has its own subclass that sets STATUS."""

    STATUS = ""

    def getCategories(self) -> list:
        """The categories managed by the Platform Administrator (#65-#69), for the form."""
        return IDPCategory.getCategoryNames()

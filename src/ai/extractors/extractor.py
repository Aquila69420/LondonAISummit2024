from abc import ABC, abstractmethod
from typing import List, Dict


class Extractor(ABC):
    """
    Abstract base class for an Extractor that extracts tasks from a string.

    Methods:
        extractTasks(self, text: str) -> List[Task]:
            Abstract method to extract a list of Task objects from a given string.
    """

    @abstractmethod
    def extract(self, text: str) -> Dict[str, str]:
        """
        Extracts data from the provided text.

        Args:
            text (str): The text to parse for data.

        Returns:
            Dict[str, str]: A dictionary of extracted data.
        """
        pass

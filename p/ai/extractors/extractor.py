from abc import ABC, abstractmethod
from typing import List
from pipeline.data_structures import Task


class Extractor(ABC):
    """
    Abstract base class for an Extractor that extracts tasks from a string.

    Methods:
        extractTasks(self, text: str) -> List[Task]:
            Abstract method to extract a list of Task objects from a given string.
    """

    @abstractmethod
    def extract_tasks(self, text: str) -> List[Task]:
        """
        Extracts tasks from the provided text.

        Args:
            text (str): The text to parse for task information.

        Returns:
            List[Task]: A list of extracted Task objects.
        """
        pass

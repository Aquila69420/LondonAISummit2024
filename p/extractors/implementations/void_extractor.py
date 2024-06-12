from typing import List
from ..extractor import Extractor
from pipeline.data_structures import Task


class VoidExtractor(Extractor):
    """
    A void extractor that simple returns an empty list of tasks.
    This is useful when you want to skip the extraction step in the pipeline.
    Can be used for testing purposes.
    """
    def extract_tasks(self, text: str) -> List[Task]:
        return []

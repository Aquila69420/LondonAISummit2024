import re
from typing import List, Dict
from ..extractor import Extractor


class JsonExtractor(Extractor):
    """
    Tries to extract tasks from the text assuming it tries to follow a JSON format (doesn't have to be valid JSON).
    """

    def __init__(self, key: [str]):
        """
        Create a new JSON extracts, this extractor expects the output to look like JSON with specific keys
        :param key: List of keys that the JSON schema contains
        """
        self.key: [str] = key
        pass

    def extract_tasks(self, text: str) -> Dict[str, str]:
        print("Extracting tasks from JSON text.")

        current_object = {}
        missing_key = self.key.copy()

        for line in text.split("\n"):
            line = line.strip()
            for key in missing_key:
                pattern = f'"{key}"' + ': "([^}]*)"'
                matches = re.findall(pattern, line)
                if len(matches) == 0:
                    continue
                missing_key.remove(key)
                current_object[key] = matches[0]
                break

            if len(missing_key) == 0:
                return current_object

        return current_object

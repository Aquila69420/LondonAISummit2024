import re
from typing import List, Dict
from ..extractor import Extractor


class JsonExtractor(Extractor):
    """
    Tries to extract tasks from the text assuming it tries to follow a JSON format (doesn't have to be valid JSON).
    """

    def __init__(self, key: [str], key_map: Dict[str, str] | None = None):
        """
        Create a new JSON extracts, this extractor expects the output to look like JSON with specific keys
        A key mop can be provided to map JSON key to the expected task field names
        :param key: List of keys that the JSON schema contains
        :param key_map: Map of JSON keys to task field names, if matches exactly you dont have to provided one
        """
        self.key: [str] = key
        self.key_map: Dict[str, str] | None = key_map
        pass

    def _convert_obj_task(self, obj: Dict[str, str]) -> Task:
        # Apply name mapping if one is give
        if self.key_map is not None:
            pobj = {}
            for key in obj.keys():
                if key not in self.key_map.keys(): # If no mapping exists for this key just carry it over
                    pobj[key] = obj[key]
                else:
                    pobj[self.key_map[key]] = obj[key]
        else:
            pobj = obj

        task = Task(
            pobj['Name'],
            pobj['Description'],
            DateTimeParser.try_parse_date(pobj['DueDate']),
            DateTimeParser.try_parse_date(pobj['DueTime'])
        )

        return task

    def extract_tasks(self, text: str) -> List[Task]:
        print("Extracting tasks from JSON text.")

        res = []
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
                res.append(current_object)
                current_object = {}
                missing_key = self.key.copy()

        return [self._convert_obj_task(obj) for obj in res]

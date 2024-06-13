import re
from .erf_environment import ERFEnvironment
from pathlib import Path
from typing import Union, Dict


class ERFCompiler:
    """
    ERF compiler reads in a .erf file and outputs raw text after all references have been resolved.
    """
    def __init__(self, environment: ERFEnvironment):
        """
        Initialize the compiler with an environment.
        """
        self.environment: ERFEnvironment = environment

    def compile(self, erf_file: Union[str, Path]) -> str:
        """
        Compile the given .erf file and return the processed text.

        :param erf_file: The path to the .erf file to compile (as a string or Path object).
        :return: The compiled text.
        """
        # Ensure the input is a Path object
        if isinstance(erf_file, str):
            erf_file = Path(erf_file)

        # Check if the path is valid if it's a root file
        if not self._is_path_valid(erf_file):
            raise FileNotFoundError(f"File not found: {erf_file}")

        # Read the files contents
        with erf_file.open() as file:
            contents = file.read()

        # Find all possible references
        placeholders = self._find_placeholders(contents)

        # Resolve all references
        for placeholder, value in placeholders.items():
            if not self._is_placeholder_erf(placeholder):
                continue  # Skip non-ERF placeholders, it could be a placeholder for another system
            resolved_value = self._resolve_erf_placeholder(value)
            contents = contents.replace(placeholder, resolved_value)

        return contents

    def _resolve_erf_placeholder(self, placeholder: str) -> str:
        """
        Resolve the given ERF placeholder.

        :param placeholder: The ERF placeholder to resolve.
        :return: The resolved value.
        """
        if self._is_path_valid(placeholder):
            return self.compile(placeholder)
        else:  # Placeholder is an environment variable
            if placeholder not in self.environment.env_vars:
                raise ValueError(f"ERF Environment variable not found: {placeholder}")
            return self.environment.env_vars[placeholder]

    @staticmethod
    def _is_path_valid(path: Union[Path, str]) -> bool:
        """
        Check if the given path is valid.

        :param path: The path to check.
        :return: True if the path is valid, False otherwise.
        """
        # Ensure path is a Path object
        if isinstance(path, str):
            path = Path(path)
        # Check if the path exists and is a file
        return path.exists() and path.is_file()

    @staticmethod
    def _find_placeholders(text: str) -> Dict[str, str]:
        """
        Find all placeholders in the given text that are formatted as {ERF:content}.

        :param text: The text to search for placeholders.
        :return: A dictionary of placeholders in the format {ERF:content} and their plain content.
        """
        # Regex pattern to find content enclosed in {} and starting with 'ERF:'
        pattern = r'\{ERF:([^}]*)\}'
        matches = re.findall(pattern, text)
        tagged_elements = {f'{{ERF:{match}}}': match for match in matches}
        return tagged_elements

    @staticmethod
    def _is_placeholder_erf(placeholder: str) -> bool:
        """
        Check if the given placeholder is an ERF placeholder.

        :param placeholder: The placeholder to check.
        :return: True if the placeholder is an ERF placeholder, False otherwise.
        """
        return placeholder.startswith('{ERF:')

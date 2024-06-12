from abc import ABC, abstractmethod
from dataclasses import dataclass


class PromptInjector(ABC):
    """
    Abstract base class for a PromptInjector that injects data into prompt templates.

    Attributes:
        prompt_template (PromptTemplate): The template used for generating prompts.

    Methods:
        inject_prompt(self, data: str) -> str:
            Abstract method to inject data into the prompt template and return a complete prompt.
    """

    def __init__(self, prompt_template: str):
        """
        Initializes the PromptInjector with a prompt template.
        :param prompt_template: The template used for generating prompts.
        """
        self.prompt_template: str = prompt_template

    @abstractmethod
    def inject_prompt(self, data: str) -> str:
        """
        Injects data into the prompt template and returns the complete prompt.

        Args:
            data (str): The data to be injected into the prompt template.

        Returns:
            str: The final prompt string after data injection.
        """
        pass

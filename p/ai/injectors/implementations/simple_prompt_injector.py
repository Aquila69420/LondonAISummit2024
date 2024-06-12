from typing import Dict

from ..prompt_injector import PromptInjector


class SimplePromptInjector(PromptInjector):
    """
    A simple implementation of a PromptInjector that injects data into a prompt template
    using string formatting and is expecting the template to have a placeholder called 'data'.
    """
    def __init__(self, prompt_template: str):
        super().__init__(prompt_template)

    def inject_prompt(self, input_data: Dict[str, str]) -> str:
        return self.prompt_template.format(**input_data)

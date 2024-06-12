from ..prompt_injector import PromptInjector


class SimplePromptInjector(PromptInjector):
    """
    A simple implementation of a PromptInjector that injects data into a prompt template
    using string formatting and is expecting the template to have a placeholder called 'data'.
    """
    def inject_prompt(self, data: str) -> str:
        return self.prompt_template.format(data=data)

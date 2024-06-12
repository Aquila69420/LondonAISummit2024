from ..llm_model import LLMModel

class VoidModel(LLMModel):
    """
    A void model simply takes in the input and returns it as the output without any processing.
    This is useful for testing and debugging purposes.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)

    def start_chat(self):
        pass

    def end_chat(self):
        pass

    def send_message(self, message: str) -> str:
        return ""

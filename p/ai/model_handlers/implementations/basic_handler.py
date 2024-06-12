from ..model_handler import ModelHandler
from ai.models import LLMModel
from typing import Union


class BasicHandler(ModelHandler):
    """
    BasicHandler is a class that wraps around a LLMModel to provide a more interface that handles priming messages.
    """

    def __init__(self, model: LLMModel, priming_message: Union[None, str]):
        super().__init__(model, priming_message)

    def send_message(self, message: str, skip_priming: bool = False, debug: bool = False) -> str:
        if self._first_message and self.priming_message is not None and not skip_priming:
            priming_reply = self.model.send_message(self.priming_message)
            self._first_message = False
            if debug:
                print(f"Priming message reply: {priming_reply}")

        return self.model.send_message(message)

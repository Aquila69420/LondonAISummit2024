from ai.models import LLMModel
from typing import Union


class ModelHandler:
    """
    ModelHandler is a class that wraps around a LLMModel to provide a more interface.
    """

    def __init__(self, model: LLMModel, priming_message: Union[None, str]):
        """
        Initialize the ModelHandler with a model and a priming message.

        :param model: Model to wrap around.
        :param priming_message: Priming message to use when starting the model.
        """
        self._first_message = True
        self.model: LLMModel = model
        self.priming_message: str | None = priming_message

    def send_message(self, message: str, skip_priming: bool = False, debug: bool = False) -> str:
        """
        Send a message to the model.

        :param message: The message to send to the model.
        :param skip_priming: If True, the priming message will not be sent, even if it is the first message.
        :param debug: If True, the reply to a priming message will be printed when a priming message is sent.
        :return: The response from the model.
        """
        raise NotImplementedError

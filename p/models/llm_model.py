from abc import ABC, abstractmethod


class LLMModel(ABC):
    """
    Abstract base class for a large language model (LLM) interface.

    Attributes:
        model_name (str): The name of the model.
        primer (PrimingMessage): A priming message to initialize or set the context for the model.

    Methods:
        startChat(self): Starts a chat session.
        endChat(self): Ends a chat session.
        sendMessage(self): Sends a message and returns a response from the model.
    """

    def __init__(self, model_name: str):
        """
        Initializes the LLMModel with a model name and a priming message.

        Args:
            model_name (str): The name of the model.
        """
        self.model_name = model_name

    @abstractmethod
    def start_chat(self):
        """
        Abstract method to start a chat session.
        This should also initialize any api connections and resources used by the model.
        """
        pass

    @abstractmethod
    def end_chat(self):
        """
        Abstract method to end a chat session.
        This should also close any api connections and resources used by the model.
        """
        pass

    @abstractmethod
    def send_message(self, message: str) -> str:
        """
        Abstract method to send a message and receive a response from the model.

        Args:
            message (str): The message to send to the model.

        Returns:
            str: The response from the model.
        """
        pass

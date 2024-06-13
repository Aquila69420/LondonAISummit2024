from ..llm_model import LLMModel
import google.generativeai as genai


class GeminiModel(LLMModel):
    """
    API interface for the Gemini model.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini model with an API key and model name.
        :param api_key: Key for the Gemini API.
        :param model_name: Name of the model to use, default is "gemini-1.5-flash" and it most match models available in the Gemini API.
        """
        super().__init__(model_name)
        genai.configure(api_key=api_key)
        self.model = None
        self.chat = None

    def start_chat(self):
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat()

    def end_chat(self):
        self.chat = None
        self.model = None

    def send_message(self, message: str) -> str:
        assert self.model is not None, "Model is not initialized. Call start_chat() before sending messages."
        response = self.chat.send_message(message)
        return response.text

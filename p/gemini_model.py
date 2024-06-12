import google.generativeai as genai


class GeminiModel:
    """
    API interface for the Gemini model.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini model with an API key and model name.
        :param api_key: Key for the Gemini API.
        :param model_name: Name of the model to use, default is "gemini-1.5-flash" and it most match models available in the Gemini API.
        """
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = None

    def start_chat(self):
        self.model = genai.GenerativeModel(self.model_name)

    def end_chat(self):
        self.model = None

    def send_message(self, message: str) -> str:
        assert self.model is not None, "Model is not initialized. Call start_chat() before sending messages."
        response = self.model.generate_content(message)
        return response.text

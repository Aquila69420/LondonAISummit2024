from ..models import GeminiModel, LLMModel
from ..model_handlers import BasicHandler, ModelHandler
from ..injectors import SimplePromptInjector, PromptInjector
from erf import ERFEnvironment, ERFCompiler


class UnderstandPrtPipeline:
    """
    A pipeline that preprocesses PRT schema data
    """

    def __init__(self, key: str, gemini_model: str = "gemini-1.5-flash"):
        erf_compiler = ERFCompiler(ERFEnvironment())
        primer = erf_compiler.compile("templates\\primers\\understand_prt.ert")
        prompt = erf_compiler.compile("templates\\prompts\\understand_prt.ert")

        self.prompt_injector: PromptInjector = SimplePromptInjector(prompt)
        model: LLMModel = GeminiModel(key, gemini_model)
        model.start_chat()
        self.model_handler: ModelHandler = BasicHandler(model, primer)

    def process(self, input_data: str):
        prompt = self.prompt_injector.inject_prompt({'data': input_data})
        model_out = self.model_handler.send_message(prompt)
        return model_out

    def __del__(self):
        self.model_handler.model.end_chat()

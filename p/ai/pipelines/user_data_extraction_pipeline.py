from ..models import GeminiModel, LLMModel
from ..model_handlers import BasicHandler, ModelHandler
from ..injectors import SimplePromptInjector, PromptInjector
from ..extractors import Extractor, JsonExtractor
from erf import ERFEnvironment, ERFCompiler


class UserDataExtractionPipeline:
    """
    This pipeline is responsible for extracting user data from any format to a structured from that follows JSON.
    """

    def __init__(self, key: str, gemini_model: str = "gemini-1.5-flash"):
        erf_compiler = ERFCompiler(ERFEnvironment())
        primer = erf_compiler.compile("templates\\primers\\user_input_extraction.erf")
        prompt = erf_compiler.compile("templates\\prompts\\user_input_extraction.erf")
        expected_fields = ['Date of Birth', 'Date joined company', 'Gender', 'Marital Status', 'Pension Status',
                           'No. of Children', 'Retirement Date', 'Retirement Type', 'Current Pension Amount']

        self.prompt_injector: PromptInjector = SimplePromptInjector(prompt)
        model: LLMModel = GeminiModel(key, gemini_model)
        model.start_chat()
        self.model_handler: ModelHandler = BasicHandler(model, primer)
        self.extractor: Extractor = JsonExtractor(expected_fields)

    def process(self, input_data: str):
        prompt = self.prompt_injector.inject_prompt({'data': input_data})
        model_out = self.model_handler.send_message(prompt)
        out_processed = self.extractor.extract(model_out)
        print(out_processed)
        return out_processed

    def __del__(self):
        self.model_handler.model.end_chat()

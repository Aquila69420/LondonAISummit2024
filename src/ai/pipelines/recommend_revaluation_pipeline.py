from typing import Dict

from ..models import GeminiModel, LLMModel
from ..model_handlers import BasicHandler, ModelHandler
from ..injectors import SimplePromptInjector, PromptInjector
from ..extractors import Extractor, JsonExtractor
from erf import ERFEnvironment, ERFCompiler


class RecommendRevaluationPipeline:
    """
    A pipeline responsible for recommending revaluation of a user's pension.
    """

    def __init__(self, key: str, year: str, gemini_model: str = "gemini-1.5-flash"):
        efr_env = ERFEnvironment()
        efr_env.env_vars['year'] = year
        erf_compiler = ERFCompiler(efr_env)
        primer = erf_compiler.compile("templates\\primers\\recommend_revaluation.erf")
        prompt = erf_compiler.compile("templates\\prompts\\recommend_revaluation.erf")
        self.explain_prompt = erf_compiler.compile("templates\\prompts\\explain.txt")
        expected_fields = ['Criteria', 'Description', 'Adjustment about', 'Amount']

        self.prompt_injector: PromptInjector = SimplePromptInjector(prompt)
        model: LLMModel = GeminiModel(key, gemini_model)
        model.start_chat()
        self.model_handler: ModelHandler = BasicHandler(model, primer)
        self.extractor: Extractor = JsonExtractor(expected_fields)

    def process(self, input_data: str, prt_data: str) -> Dict[str, str]:
        prompt = self.prompt_injector.inject_prompt({'user_data': input_data, 'prt_data': prt_data})
        model_out = self.model_handler.send_message(prompt)
        out_processed = self.extractor.extract(model_out)
        out_processed['Explanation'] = self.model_handler.send_message(self.explain_prompt)
        return out_processed

    def __del__(self):
        self.model_handler.model.end_chat()

from uagents import Agent, Context
from .data_structures import TextReply, DictionaryReply, DataFromChainRecommendation, ChainDictReply, \
    DataForRecommendation
import agents
from ai import UnderstandPrtPipeline

MULTI_YEAR_CHAIN_ADDRESS: str | None = None
agent = Agent(name="multi_year_chain_agent", seed="multi_year_chain_agent recovery phrase")
_processed_user_data = None
_processed_scheme_data = None
_recommendation_stack = []
_remaining_chain_length = None
_sender: str | None = None
_current_data: DataForRecommendation | None = None


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info("started")
    global MULTI_YEAR_CHAIN_ADDRESS
    MULTI_YEAR_CHAIN_ADDRESS = agent.address


@agent.on_message(model=DataFromChainRecommendation)
async def message_handler(ctx: Context, sender: str, msg: DataFromChainRecommendation):
    global _remaining_chain_length, _sender, _current_data, _recommendation_stack
    _recommendation_stack = []
    _sender = sender
    _remaining_chain_length = msg.chain_length - 1
    _current_data = msg.base_input

    ctx.logger.info(f"Received message from {sender}")
    await ctx.send(agents.recommendation_agent.RECOMMENDATION_AGENT_ADDRESS, _current_data, timeout=None, sync=True)
    _current_data.current_year += 1


@agent.on_message(model=DictionaryReply)
async def message_handler(ctx: Context, sender: str, msg: DictionaryReply):
    global _processed_user_data, _recommendation_stack, _recommendation_stack, _sender, _remaining_chain_length, _current_data
    if sender == agents.recommendation_agent.RECOMMENDATION_AGENT_ADDRESS:
        _recommendation_stack.append(msg.dictionary)
        print(msg.dictionary)

    if _remaining_chain_length == 0:
        await ctx.send(_sender, ChainDictReply(dict_chain=_remaining_chain_length), timeout=None, sync=True)
    else:
        _remaining_chain_length -= 1
        await ctx.send(agents.recommendation_agent.RECOMMENDATION_AGENT_ADDRESS, _current_data, timeout=None, sync=True)
        _current_data.current_year += 1


def run():
    agent.run()

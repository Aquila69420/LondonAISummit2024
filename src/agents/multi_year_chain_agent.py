from uagents import Agent, Context
from .data_structures import PensionSchemeData, TextReply
from ai import UnderstandPrtPipeline

MULTI_YEAR_CHAIN_ADDRESS: str | None = None
agent = Agent(name="multi_year_chain_agent", seed="multi_year_chain_agent recovery phrase")
_processed_user_data = None
_processed_scheme_data = None
_recommendation_stack = []

@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info("started")
    global MULTI_YEAR_CHAIN_ADDRESS
    MULTI_YEAR_CHAIN_ADDRESS = agent.address


@agent.on_message(model=PensionSchemeData)
async def message_handler(ctx: Context, sender: str, msg: PensionSchemeData):
    ctx.logger.info(f"Received message from {sender}")
    pipe = UnderstandPrtPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    out = pipe.process(msg.raw_pension_scheme_data)
    await ctx.send(sender, TextReply(text=out), timeout=None, sync=True)


def run():
    agent.run()

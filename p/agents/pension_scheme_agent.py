from uagents import Agent, Context
from .data_structures import PensionSchemeData, TextReply
from ai import UserDataExtractionPipeline

PENSION_SCHEME_ADDRESS: str | None = None
agent = Agent(name="pension_scheme_agent", seed="pension_scheme_agent recovery phrase")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    print("pension_scheme_agent started")
    global PENSION_SCHEME_ADDRESS
    PENSION_SCHEME_ADDRESS = agent.address


@agent.on_message(model=PensionSchemeData)
async def message_handler(ctx: Context, sender: str, msg: PensionSchemeData):
    print(f"user_input_agent received message from {sender}: {msg.raw_pension_scheme_data}")
    pipe = UserDataExtractionPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    out = pipe.process(msg.raw_pension_scheme_data)
    await ctx.send(sender, TextReply(text=out), timeout=None, sync=True)


def run():
    agent.run()

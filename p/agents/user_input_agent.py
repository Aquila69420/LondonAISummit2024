from uagents import Agent, Context
from data_structures import UserRawData, DictionaryReply
from ai import UserDataExtractionPipeline

USER_INPUT_AGENT_ADDRESS: str | None = None
agent = Agent(name="user_input_agent", seed="user_input_agent recovery phrase")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    global USER_INPUT_AGENT_ADDRESS
    USER_INPUT_AGENT_ADDRESS = agent.address


@agent.on_message(model=UserRawData)
async def message_handler(ctx: Context, sender: str, msg: UserRawData):
    print(f"user_input_agent received message from {sender}: {msg.raw_user_data}")
    pipe = UserDataExtractionPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    out = pipe.process(msg.raw_user_data)
    await ctx.send(sender, DictionaryReply(text=out), timeout=None, sync=True)


def run():
    agent.run()

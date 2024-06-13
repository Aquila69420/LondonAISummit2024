from uagents import Agent, Context
from agents import *
from agents.user_input_agent import USER_INPUT_AGENT_ADDRESS
from .data_structures import *

agent = Agent(name="coordinator_agent", seed="coordinator_agent recovery phrase")
_processed_user_data = None
_processed_scheme_data = None
_recommendation = None


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    print("coordinator_agent started")
    test = ("Tom not married, current pension 50000, tom is a dad had a "
            "son Bob and daughter Elsa and has retired normally.")
    #await ctx.send(USER_INPUT_AGENT_ADDRESS, UserRawData(test), timeout=None, sync=True)


@agent.on_message(model=DictionaryReply)
async def message_handler(ctx: Context, sender: str, msg: DictionaryReply):
    print(msg.dictionary)

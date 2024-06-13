import time

from uagents import Agent, Context

import agents.user_input_agent
from agents import *
from .data_structures import *

agent = Agent(name="coordinator_agent", seed="coordinator_agent recovery phrase")
_processed_user_data = None
_processed_scheme_data = None
_recommendation = None


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info("started")
    test = ("Tom not married, current pension 50000, tom is a dad had a "
            "son Bob and daughter Elsa and has retired normally.")
    #await ctx.send(USER_INPUT_AGENT_ADDRESS, UserRawData(test), timeout=None, sync=True)


a = False
@agent.on_interval(period=2.0)
async def send_message(ctx: Context):
    global a
    if a:
        return
    a = True
    test = ("Tom not married, current pension 50000, tom is a dad had a "
            "son Bob and daughter Elsa and has retired normally.")
    await ctx.send(agents.user_input_agent.USER_INPUT_AGENT_ADDRESS, UserRawData(raw_user_data=test), timeout=None, sync=True)


@agent.on_message(model=DictionaryReply)
async def message_handler(ctx: Context, sender: str, msg: DictionaryReply):
    print(msg.dictionary)

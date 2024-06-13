import time

from uagents import Agent, Context

import agents.user_input_agent
from agents import *
from custome_io import read_docx
from .data_structures import *

agent = Agent(name="coordinator_agent", seed="coordinator_agent recovery phrase")
_processed_user_data = None
_processed_scheme_data = None
_recommendation = None


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info("started")

    test1 = ("Tom not married, current pension 50000, tom is a dad had a "
             "son Bob and daughter Elsa and has retired normally.")
    test2 = read_docx("input/IBP_Problemstatement.docx")
    await ctx.send(agents.user_input_agent.USER_INPUT_AGENT_ADDRESS, UserRawData(raw_user_data=test1), timeout=None,
                   sync=False)
    await ctx.send(agents.pension_scheme_agent.PENSION_SCHEME_ADDRESS, PensionSchemeData(raw_pension_scheme_data=test2),
                   timeout=None,
                   sync=False)


@agent.on_message(model=DictionaryReply)
async def message_handler(ctx: Context, sender: str, msg: DictionaryReply):
    global _processed_user_data, _recommendation
    if sender == agents.user_input_agent.USER_INPUT_AGENT_ADDRESS:
        _processed_user_data = msg.dictionary
        #print(_processed_user_data)
    elif sender == agents.recommendation_agent.RECOMMENDATION_AGENT_ADDRESS:
        _recommendation = msg.dictionary
        print(_recommendation)


@agent.on_message(model=TextReply)
async def message_handler(ctx: Context, sender: str, msg: TextReply):
    global _processed_scheme_data
    _processed_scheme_data = msg.text
    #print(_processed_scheme_data)

call_made = False
chained = False
@agent.on_interval(period=10.0)
async def send_message(ctx: Context):
    global _processed_user_data, _processed_scheme_data
    if _processed_user_data is not None and _processed_scheme_data is not None:
        await ctx.send(agents.recommendation_agent.RECOMMENDATION_AGENT_ADDRESS,
                       DataForRecommendation(processed_user_data=_processed_user_data,
                                             processed_scheme=_processed_scheme_data,
                                             current_year="1987"), timeout=None, sync=True)


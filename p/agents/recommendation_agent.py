from uagents import Agent, Context
from .data_structures import DataForRecommendation, DictionaryReply
from ai import RecommendRevaluationPipeline

RECOMMENDATION_AGENT_ADDRESS: str | None = None
agent = Agent(name="recommendation_agent", seed="recommendation_agent recovery phrase")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info("started")
    global RECOMMENDATION_AGENT_ADDRESS
    RECOMMENDATION_AGENT_ADDRESS = agent.address


@agent.on_message(model=DataForRecommendation)
async def message_handler(ctx: Context, sender: str, msg: DataForRecommendation):
    ctx.logger.info(f"Received message from {sender}: {msg.processed_user_data}")
    pipe = RecommendRevaluationPipeline("AIzaSyCO8QBl6pLBM3XIxh33voc0JlC5w0J6AAU")
    out = pipe.process(str(msg.processed_user_data), msg.processed_scheme)

    ####################################
    # Try to calculate the new pension #
    ####################################
    initial_pension = None
    adjustment = None
    recalculation = None
    try:
        initial_pension = float(msg.processed_user_data['Current Pension Amount'])
        adjustment = float(out['Amount'])
    except KeyError:
        pass
    if initial_pension is not None and adjustment is not None:
        recalculation = initial_pension * (1 + adjustment)

    #######################################################
    # Try to create the explanation for the agents action #
    #######################################################
    criteria = out['Criteria'] if 'Criteria' in out else ""
    description = out['Description'] if 'Description' in out else ""
    adjustment = out['Adjustment about'] if 'Adjustment about' in out else ""
    explanation = f"{criteria}\n{description}\n{adjustment}"

    #############################
    # Stitch the reply together #
    #############################
    res = {
        "Initial": initial_pension if initial_pension is not None else "Missing",
        "Adjusted": recalculation if recalculation is not None else "Not enough data to calculate",
        "Explanation": explanation
    }

    await ctx.send(sender, DictionaryReply(dictionary=res), timeout=None, sync=True)


def run():
    agent.run()

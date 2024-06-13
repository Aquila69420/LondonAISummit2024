from uagents import Agent, Context

RECOMMENDATION_AGENT_ADDRESS: str | None = None
agent = Agent(name="recommendation_agent", seed="recommendation_agent recovery phrase")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    global RECOMMENDATION_AGENT_ADDRESS
    RECOMMENDATION_AGENT_ADDRESS = agent.address


def run():
    agent.run()

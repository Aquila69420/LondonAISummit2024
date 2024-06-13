from uagents import Agent, Context

PENSION_SCHEME_ADDRESS: str | None = None
agent = Agent(name="pension_scheme_agent", seed="pension_scheme_agent recovery phrase")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    global PENSION_SCHEME_ADDRESS
    PENSION_SCHEME_ADDRESS = agent.address


def run():
    agent.run()

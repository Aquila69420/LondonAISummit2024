from uagents import Agent, Bureau, Context, Model

USER_INPUT_AGENT_ADDRESS: str | None = None
agent = Agent(name="user_input_agent", seed="user_input_agent recovery phrase")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    global USER_INPUT_AGENT_ADDRESS
    USER_INPUT_AGENT_ADDRESS = agent.address

@agent.on_message(model=Message)
async def bob_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(alice.address, Message(message="hello there alice"))

def run():
    agent.run()

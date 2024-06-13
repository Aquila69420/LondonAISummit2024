from . import coordinator_agent
from .user_input_agent import USER_INPUT_AGENT_ADDRESS
from .pension_scheme_agent import PENSION_SCHEME_ADDRESS
from .recommendation_agent import RECOMMENDATION_AGENT_ADDRESS
from uagents import Bureau

bureau = Bureau()
bureau.add(user_input_agent.agent)
bureau.add(pension_scheme_agent.agent)
bureau.add(recommendation_agent.agent)
bureau.add(coordinator_agent.agent)


__all__ = ["USER_INPUT_AGENT_ADDRESS", "PENSION_SCHEME_ADDRESS", "RECOMMENDATION_AGENT_ADDRESS"]
bureau.run()

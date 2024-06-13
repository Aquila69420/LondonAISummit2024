from . import coordinator_agent
from . import user_input_agent
from . import pension_scheme_agent
from . import recommendation_agent
from uagents import Bureau

bureau = Bureau()
bureau.add(user_input_agent.agent)
bureau.add(pension_scheme_agent.agent)
bureau.add(recommendation_agent.agent)
bureau.add(coordinator_agent.agent)
bureau.run()

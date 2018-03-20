from .agent import Agent
from .commodities import glass_consumer,glass_maker,sand_digger


class Market(object):
    _agents = None

    def __init__(self, num_agents=15):
        self._agents = []

        for i in range(0, round(num_agents/3), 3):
            self._agents.append(Agent(sand_digger))
            self._agents.append(Agent(glass_maker))
            self._agents.append(Agent(glass_consumer))


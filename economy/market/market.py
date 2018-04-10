import random


from economy.agent import Agent,dump_agent
from economy import goods
from economy.market.book import OrderBook
from economy.market.history import MarketHistory
from economy.offer import Ask,Bid


class Market(object):
    _agents = None
    _book = None
    _history = None

    def __init__(self, num_agents=15):
        self._agents = []
        self._book = OrderBook()
        self._history = MarketHistory()

        for recipe in [goods.sand_digger, goods.glass_maker, goods.glass_consumer]:
            for i in range(0, num_agents, 3):
                self._agents.append(Agent(recipe))

    def simulate(self, steps=1):
        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

        for day in range(steps):
            self._history.open_day()
            self._book.clear_books()

            for agent in self._agents:
                self._book.add_orders(agent.make_offers())
                agent.do_production()

            for good in goods.all():
                trades = self._book.resolve_orders(good)
                self._history.add_trades(good, trades)

            self._history.close_day()

        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

        self._agents[:] = [agent for agent in self._agents if not agent.is_bankrupt]

    def history(self, depth=None):
        return self._history.history(depth)

    def aggregate(self, good, depth=None):
        return self._history.aggregate(good, depth)


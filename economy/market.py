import random


from .agent import Agent
from .commodities import glass_consumer,glass_maker,sand_digger
from .offer import Ask,Bid


class OrderBook(object):
    def __init__(self):
        self.clear_books()

    def clear_books(self):
        self._asks = []
        self._bids = []

    def add_order(self, order):
        if isinstance(order, Ask):
            self._asks.append(order)
        elif isinstance(order, Bid):
            self._bids.append(order)
        else:
            raise ValueError("Order is not an Ask or a Bid")

    def add_orders(self, orders):
        for order in orders:
            self.add_order(order)

    def resolve_orders(self):
        # First shuffle the orders to ensure Agent ordering not a factor
        random.shuffle(self._asks)
        random.shuffle(self._bids)

        # Now sort by price
        self._asks.sort(key=lambda o: o.unit_price, reverse=True)
        self._bids.sort(key=lambda o: o.unit_price)

        while self._asks and self._bids:
            ask = self._asks.pop()
            bid = self._bids.pop()

            qty = min(ask.units, bid.units)
            price = qty * int((ask.unit_price + bid.unit_price)/2)

            print("Bid: {} units of {} for {}; Ask: {} units of {} for {}".format(
                bid.units, bid.commodity, bid.unit_price,
                ask.units, ask.commodity, ask.unit_price,
                ))


class Market(object):
    _agents = None
    _book = None

    def __init__(self, num_agents=15):
        self._agents = []
        self._book = OrderBook()

        for i in range(0, num_agents, 3):
            self._agents.append(Agent(sand_digger))
            self._agents.append(Agent(glass_maker))
            self._agents.append(Agent(glass_consumer))

    def simulate(self, steps=1):
        for day in range(steps):
            self._book.clear_books()

            for agent in self._agents:
                self._book.add_orders(agent.make_offers())
                agent.do_production()

            self._book.resolve_orders()


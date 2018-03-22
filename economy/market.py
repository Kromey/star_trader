import random


from .agent import Agent,dump_agent
from . import commodities
from .offer import Ask,Bid


class OrderBook(object):
    def __init__(self):
        self.clear_books()

    def clear_books(self):
        self._asks = {}
        self._bids = {}

    def add_order(self, order):
        if isinstance(order, Ask):
            if order.commodity not in self._asks:
                self._asks[order.commodity] = []
            self._asks[order.commodity].append(order)
        elif isinstance(order, Bid):
            if order.commodity not in self._bids:
                self._bids[order.commodity] = []
            self._bids[order.commodity].append(order)
        else:
            raise ValueError("Order is not an Ask or a Bid")

    def add_orders(self, orders):
        for order in orders:
            self.add_order(order)

    def resolve_orders(self, commodity):
        asks = self._asks.get(commodity, [])
        bids = self._bids.get(commodity, [])

        # First shuffle the orders to ensure Agent ordering not a factor
        random.shuffle(asks)
        random.shuffle(bids)

        # Now sort by price
        asks.sort(key=lambda o: o.unit_price, reverse=True)
        bids.sort(key=lambda o: o.unit_price)

        while asks and bids:
            ask = asks.pop()
            bid = bids.pop()

            qty = min(ask.units, bid.units)
            price = int((ask.unit_price + bid.unit_price)/2)

            bid.agent.give_money(qty * price, ask.agent)
            ask.agent.give_items(commodity, qty, bid.agent)

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
            self._agents.append(Agent(commodities.sand_digger))
            self._agents.append(Agent(commodities.glass_maker))
            self._agents.append(Agent(commodities.glass_consumer))

    def simulate(self, steps=1):
        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

        for day in range(steps):
            self._book.clear_books()

            for agent in self._agents:
                self._book.add_orders(agent.make_offers())
                agent.do_production()

            for commodity in commodities.all():
                self._book.resolve_orders(commodity)

        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)


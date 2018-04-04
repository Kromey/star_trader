import random


from .agent import Agent,dump_agent
from . import goods
from .offer import Ask,Bid


class OrderBook(object):
    def __init__(self):
        self.clear_books()

    def clear_books(self):
        self._asks = {}
        self._bids = {}

    def add_order(self, order):
        if isinstance(order, Ask):
            if order.good not in self._asks:
                self._asks[order.good] = []
            self._asks[order.good].append(order)
        elif isinstance(order, Bid):
            if order.good not in self._bids:
                self._bids[order.good] = []
            self._bids[order.good].append(order)
        else:
            raise ValueError("Order is not an Ask or a Bid")

    def add_orders(self, orders):
        for order in orders:
            self.add_order(order)

    def resolve_orders(self, good):
        asks = self._asks.get(good, [])
        bids = self._bids.get(good, [])

        units_sold = 0
        total_value = 0

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

            units_sold += qty
            total_value += qty*price

            bid.agent.give_money(qty * price, ask.agent)
            ask.agent.give_items(good, qty, bid.agent)

            bid.agent.update_price_beliefs(good, price)
            ask.agent.update_price_beliefs(good, price)

            print("Bid: {} units of {} for {}; Ask: {} units of {} for {}".format(
                bid.units, bid.good, bid.unit_price,
                ask.units, ask.good, ask.unit_price,
                ))

        if units_sold > 0:
            unit_price = int(total_value/units_sold)

            while asks:
                # Unsuccessful Asks
                ask = asks.pop()
                ask.agent.update_price_beliefs(good, unit_price, False)

            while bids:
                # Unsuccessful Bids
                bid = bids.pop()
                bid.agent.update_price_beliefs(good, unit_price, False)

            print("Sold {units} {good} at an average price of {price}".format(
                units=units_sold,
                good=good,
                price=unit_price,
            ))
        else:
            print("0 units of {good} were traded today".format(good=good))


class Market(object):
    _agents = None
    _book = None

    def __init__(self, num_agents=15):
        self._agents = []
        self._book = OrderBook()

        for i in range(0, num_agents, 3):
            self._agents.append(Agent(goods.sand_digger))
            self._agents.append(Agent(goods.glass_maker))
            self._agents.append(Agent(goods.glass_consumer))

    def simulate(self, steps=1):
        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

        for day in range(steps):
            self._book.clear_books()

            for agent in self._agents:
                self._book.add_orders(agent.make_offers())
                agent.do_production()

            for good in goods.all():
                self._book.resolve_orders(good)

        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

        self._agents[:] = [agent for agent in self._agents if not agent.is_bankrupt]


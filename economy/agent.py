from collections import namedtuple


from .offer import Ask,Bid


class Inventory(object):
    _capacity = 0
    _items = {}

    def __init__(self, capacity):
        self._capacity = capacity

    def query_inventory(self, item=None):
        if item is None:
            return sum(self._items.values())
        else:
            return self._items.get(item, 0)

    def available_space(self):
        return self._capacity - self.query_inventory()

    def add_item(self, item, qty=1):
        if self.query_inventory() + qty > self._capacity:
            raise ValueError("Not enough room in inventory")
        if self.query_inventory(item) + qty < 0:
            raise ValueError("Not enough items in inventory")

        self._items[item] = self.query_inventory(item) + qty

    def remove_item(self, item, qty=1):
        # Simply "add" the negative quantity
        self.add_item(item, abs(qty) * -1)

    def set_qty(self, item, qty):
        old_qty = self.query_inventory(item)

        try:
            self._items[item] = 0
            self.add_item(item, qty)
        except:
            self._items[item] = old_qty
            raise


class Agent(object):
    INVENTORY_SIZE = 15
    _inventory = None
    _recipe = None

    def __init__(self, recipe, initial_inv=10):
        self._recipe = recipe

        # Initialize inventory
        self._inventory = Inventory(self.INVENTORY_SIZE)
        for commodity,qty_in,qty_out in self._recipe:
            self._inventory.set_qty(commodity, int(initial_inv/len(recipe)))

    def do_production(self):
        while self._can_produce():
            for commodity,qty_in,qty_out in self._recipe:
                # Deduct any required input
                self._inventory.remove_item(commodity, qty_in)
                # Add any output
                self._inventory.add_item(commodity, qty_out)

    def make_offers(self):
        space = self._inventory.available_space()
        for commodity,qty_in,qty_out in self._recipe:
            if qty_in > 0:
                # Input into our recipe, make a bid to buy
                qty = space - self._inventory.query_inventory(commodity)
                if qty > 0:
                    yield Bid(commodity, qty, 0, self)

            if qty_out > 0:
                # We produce these, sell 'em
                qty = self._inventory.query_inventory(commodity)
                if qty > 0:
                    yield Ask(commodity, qty, 0, self)

    def _can_produce(self):
        for commodity,qty_in,qty_out in self._recipe:
            # Ensure there's enough input
            if qty_in > self._inventory.query_inventory(commodity):
                return False
            # Ensure there's room for the output
            if qty_out + self._inventory.query_inventory(commodity) > Agent.INVENTORY_SIZE:
                return False

        return True


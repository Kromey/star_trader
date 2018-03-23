from collections import namedtuple
import random


from .offer import Ask,Bid


def dump_agent(agent):
    inv = ''
    for item in agent._inventory._items:
        inv += ',{item},{qty}'.format(
                item = item,
                qty = agent._inventory.query_inventory(item),
                )

    print('{agent}{inv}'.format(
        agent = agent._name,
        inv = inv
        ))


class Inventory(object):
    _capacity = 0
    _items = None

    def __init__(self, capacity):
        self._capacity = capacity
        self._items = {}

    def query_inventory(self, item=None):
        if item is None:
            return sum(self._items.values())
        else:
            return self._items.get(item, 0)

    def available_space(self):
        return self._capacity - self.query_inventory()

    def add_item(self, item, qty=1):
        if self.query_inventory() + qty > self._capacity:
            raise ValueError("Not enough room in inventory; have {inv_qty}, tried to add {qty}".format(
                inv_qty = self.query_inventory(),
                qty = qty,
                ))
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
    _money = 0
    _name = None

    def __init__(self, recipe, initial_inv=10, initial_money=100):
        self._recipe = recipe
        self._money = initial_money
        self._name = AGENT_NAMES.pop()

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
                # We deliberately do not account for qty we're selling because
                # we don't know how many we'll actually sell in this round
                # TODO: Need to adjust Bid qty to avoid overflowing inventory
                #       if an Agent requires multiple inputs
                # TODO: Agents should be reluctant to buy while prices are high
                qty = space
                if qty > 0:
                    yield Bid(commodity, qty, random.randint(0,100), self)

            if qty_out > 0:
                # We produce these, sell 'em
                # TODO: Agents should be reluctant to sell while prices are low
                qty = self._inventory.query_inventory(commodity)
                if qty > 0:
                    yield Ask(commodity, qty, random.randint(0,100), self)

    def give_money(self, amt, other):
        self._money -= amt
        other._money += amt

    def give_items(self, item, amt, other):
        self._inventory.remove_item(item, amt)
        other._inventory.add_item(item, amt)

    def _can_produce(self):
        for commodity,qty_in,qty_out in self._recipe:
            # Ensure there's enough input
            if qty_in > self._inventory.query_inventory(commodity):
                return False
            # Ensure there's room for the output
            if qty_out + self._inventory.query_inventory(commodity) > Agent.INVENTORY_SIZE:
                return False

        return True

AGENT_NAMES = [
    'James',
    'Mary',
    'John',
    'Patricia',
    'Robert',
    'Jennifer',
    'Michael',
    'Elizabeth',
    'William',
    'Linda',
    'David',
    'Barbara',
    'Richard',
    'Susan',
    'Joseph',
    'Jessica',
    'Thomas',
    'Margaret',
    'Charles',
    'Sarah',
    'Christopher',
    'Karen',
    'Daniel',
    'Nancy',
    'Matthew',
    'Betty',
    'Anthony',
    'Lisa',
    'Donald',
    'Dorothy',
    'Mark',
    'Sandra',
    'Paul',
    'Ashley',
    'Steven',
    'Kimberly',
    'Andrew',
    'Donna',
    'Kenneth',
    'Carol',
    'George',
    'Michelle',
    'Joshua',
    'Emily',
    'Kevin',
    'Amanda',
    'Brian',
    'Helen',
    'Edward',
    'Melissa',
    'Ronald',
    'Deborah',
    'Timothy',
    'Stephanie',
    'Jason',
    'Laura',
    'Jeffrey',
    'Rebecca',
    'Ryan',
    'Sharon',
    'Gary',
    'Cynthia',
    'Jacob',
    'Kathleen',
    'Nicholas',
    'Amy',
    'Eric',
    'Shirley',
    'Stephen',
    'Anna',
    'Jonathan',
    'Angela',
    'Larry',
    'Ruth',
    'Justin',
    'Brenda',
    'Scott',
    'Pamela',
    'Frank',
    'Nicole',
    'Brandon',
    'Katherine',
    'Raymond',
    'Virginia',
    'Gregory',
    'Catherine',
    'Benjamin',
    'Christine',
    'Samuel',
    'Samantha',
    'Patrick',
    'Debra',
    'Alexander',
    'Janet',
    'Jack',
    'Rachel',
    'Dennis',
    'Carolyn',
    'Jerry',
    'Emma',
    'Tyler',
    'Maria',
    'Aaron',
    'Heather',
    'Henry',
    'Diane',
    'Douglas',
    'Julie',
    'Jose',
    'Joyce',
    'Peter',
    'Evelyn',
    'Adam',
    'Frances',
    'Zachary',
    'Joan',
    'Nathan',
    'Christina',
    'Walter',
    'Kelly',
    'Harold',
    'Victoria',
    'Kyle',
    'Lauren',
    'Carl',
    'Martha',
    'Arthur',
    'Judith',
    'Gerald',
    'Cheryl',
    'Roger',
    'Megan',
    'Keith',
    'Andrea',
    'Jeremy',
    'Ann',
    'Terry',
    'Alice',
    'Lawrence',
    'Jean',
    'Sean',
    'Doris',
    'Christian',
    'Jacqueline',
    'Albert',
    'Kathryn',
    'Joe',
    'Hannah',
    'Ethan',
    'Olivia',
    'Austin',
    'Gloria',
    'Jesse',
    'Marie',
    'Willie',
    'Teresa',
    'Billy',
    'Sara',
    'Bryan',
    'Janice',
    'Bruce',
    'Julia',
    'Jordan',
    'Grace',
    'Ralph',
    'Judy',
    'Roy',
    'Theresa',
    'Noah',
    'Rose',
    'Dylan',
    'Beverly',
    'Eugene',
    'Denise',
    'Wayne',
    'Marilyn',
    'Alan',
    'Amber',
    'Juan',
    'Madison',
    'Louis',
    'Danielle',
    'Russell',
    'Brittany',
    'Gabriel',
    'Diana',
    'Randy',
    'Abigail',
    'Philip',
    'Jane',
    'Harry',
    'Natalie',
    'Vincent',
    'Lori',
    'Bobby',
    'Tiffany',
    'Johnny',
    'Alexis',
    'Logan',
    'Kayla',
]
random.shuffle(AGENT_NAMES)


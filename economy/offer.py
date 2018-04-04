

MIN_PRICE = 1


class OrderBase(object):
    _good = None
    _units = 0
    _unit_price = 0
    _agent = None

    def __init__(self, good, units, unit_price, agent):
        self._good = good
        self._units = units
        self._unit_price = max(unit_price, MIN_PRICE)
        self._agent = agent

    @property
    def good(self):
        return self._good

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    @property
    def unit_price(self):
        return self._unit_price

    @property
    def agent(self):
        return self._agent

    def __str__(self):
        return '{order}({good},{units},{unit_price})'.format(
                order = self.__class__.__name__,
                good = self.good,
                units = self.units,
                unit_price = self.unit_price,
                )


class Bid(OrderBase):
    pass


class Ask(OrderBase):
    pass




MIN_PRICE = 1


class OrderBase(object):
    _commodity = None
    _units = 0
    _unit_price = 0
    _agent = None

    def __init__(self, commodity, units, unit_price, agent):
        self._commodity = commodity
        self._units = units
        self._unit_price = max(unit_price, MIN_PRICE)
        self._agent = agent

    @property
    def commodity(self):
        return self._commodity

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
        return self.agent

    def __str__(self):
        return '{order}({commodity},{units},{unit_price})'.format(
                order = self.__class__.__name__,
                commodity = self.commodity,
                units = self.units,
                unit_price = self.unit_price,
                )


class Bid(OrderBase):
    pass


class Ask(OrderBase):
    pass


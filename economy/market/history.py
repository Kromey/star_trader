from collections import namedtuple


from economy import goods


Trades = namedtuple('Trades', ['volume', 'low', 'high', 'mean'])


class MarketHistory(object):
    def __init__(self, max_depth=30):
        self._max_depth = max_depth
        self._history = []
        self._day = []

    def open_day(self):
        self._day = []

    def add_trades(self, good, trades):
        self._day.append((good, trades))

    def close_day(self):
        self._history.append(tuple(self._day))
        self._day = []

        # Be lazy about our garbage collection
        if len(self._history) > 1.5 * self._max_depth:
            self._history = self._history[-self._max_depth:]

    @property
    def history(self, depth=None):
        if depth is None:
            depth = self._max_depth

        return self._history[-depth:]


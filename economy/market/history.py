from collections import namedtuple


from economy import goods


TradesSummary = namedtuple('TradesSummary', ['volume', 'low', 'high', 'mean'])
MarketDay = namedtuple('MarketDay', goods.all())


class MarketHistory(object):
    def __init__(self, max_depth=30):
        self._max_depth = max_depth
        self._history = []

    def add(self, day):
        self._history.append(day)

        # Be lazy about our garbage collection
        if len(self._history) > 1.5 * self._max_depth:
            self._history = self._history[-self._max_depth:]

    @property
    def history(self, depth=None):
        if depth is None:
            depth = self._max_depth

        return self._history[-depth:]


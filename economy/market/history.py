from collections import namedtuple
from functools import lru_cache
import logging


from economy import goods


logger = logging.getLogger(__name__)


Trades = namedtuple('Trades', ['volume', 'low', 'high', 'mean', 'supply', 'demand'])


class MarketHistory(object):
    def __init__(self, max_depth=30):
        self._max_depth = max_depth
        self._history = {}
        self._day = None

        for good in goods.all():
            self._history[good] = []

    def open_day(self):
        if self._day is not None:
            logger.warning('Opening new day before previous day was properly closed. Its trades have been lost. You must call close_day() to commit trades to the history.')

        self._day = {}
        for good in goods.all():
            self._day[good] = None

    def add_trades(self, good, trades):
        if self._day is None:
            logger.warning('Implicitly opening a new day to record this trade. You should call open_day() yourself.')
            self.open_day()

        self._day[good] = trades

    def close_day(self):
        for good in self._day.keys():
            self._history[good].append(self._day[good])

            # Be lazy about our garbage collection
            if len(self._history[good]) > 1.5 * self._max_depth:
                self._history[good] = self._history[good][-self._max_depth:]

        self._day = None

        # Clear our cached aggregate data
        self.aggregate.cache_clear()

    def history(self, depth=None):
        if self._day is not None:
            logger.warning('Day has been left open. It will not appear in the history.')

        if depth is None or depth > self._max_depth:
            depth = self._max_depth

        hist = {}
        for good in goods.all():
            hist[good] = self._history[good][-depth:]

        return hist

    @lru_cache(maxsize=64)
    def aggregate(self, good, depth=None):
        if self._day is not None:
            logger.warning('Day has been left open. It will not appear in the history.')

        if depth is None or depth > self._max_depth:
            depth = self._max_depth

        hist = self._history[good][-depth:]
        low = None
        high = None
        current = None

        for trades in hist:
            if trades.volume == 0:
                # No trades on this day, ignore it
                continue

            try:
                low = min(low, trades.low)
            except TypeError:
                low = trades.low

            try:
                high = max(high, trades.high)
            except TypeError:
                high = trades.high

            current = trades.mean

        try:
            ratio = (current-low)/(high-low)
        except TypeError:
            ratio = None
        except ZeroDivisionError:
            # Special case to handle high and low being the same
            ratio = 0.5

        return (low, high, current, ratio)


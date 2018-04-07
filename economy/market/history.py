from collections import namedtuple
import logging


from economy import goods


logger = logging.getLogger(__name__)


Trades = namedtuple('Trades', ['volume', 'low', 'high', 'mean'])


class MarketHistory(object):
    def __init__(self, max_depth=30):
        self._max_depth = max_depth
        self._history = []
        self._day = None

    def open_day(self):
        if self._day is not None:
            logger.warning('Opening new day before previous day was properly closed. Its trades have been lost. You must call close_day() to commit trades to the history.')

        self._day = []

    def add_trades(self, good, trades):
        if self._day is None:
            logger.warning('Implicitly opening a new day to record this trade. You should call open_day() yourself.')
            self.open_day()

        self._day.append((good, trades))

    def close_day(self):
        self._history.append(tuple(self._day))
        self._day = None

        # Be lazy about our garbage collection
        if len(self._history) > 1.5 * self._max_depth:
            self._history = self._history[-self._max_depth:]

    @property
    def history(self, depth=None):
        if self._day is not None:
            logger.warning('Day has been left open. It will not appear in the history.')

        if depth is None:
            depth = self._max_depth

        return self._history[-depth:]


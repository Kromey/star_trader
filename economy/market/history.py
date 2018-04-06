from collections import namedtuple


from economy import goods


TradesSummary = namedtuple('TradesSummary', ['volume', 'low', 'high', 'mean'])
MarketHistory = namedtuple('MarketHistory', goods.all())

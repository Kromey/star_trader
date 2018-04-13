import random


from economy.agent import Agent,dump_agent
from economy import goods,jobs
from economy.market.book import OrderBook
from economy.market.history import MarketHistory
from economy.offer import Ask,Bid


class Market(object):
    _agents = None
    _book = None
    _history = None

    def __init__(self, num_agents=15):
        self._agents = []
        self._book = OrderBook()
        self._history = MarketHistory()

        for recipe in jobs.all():
            for i in range(0, num_agents, 3):
                self._agents.append(Agent(recipe, self))

    def simulate(self, steps=1):
        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

        for day in range(steps):
            self._history.open_day()
            self._book.clear_books()

            for agent in self._agents:
                self._book.add_orders(agent.make_offers())
                agent.do_production()

            for good in goods.all():
                trades = self._book.resolve_orders(good)
                self._history.add_trades(good, trades)

            self._history.close_day()

            agents = [agent for agent in self._agents if not agent.is_bankrupt]

            while len(agents) < len(self._agents):
                jobs = {}
                for agent in agents:
                    job_profit = jobs.get(agent.job, [0, 0])
                    job_profit[0] += agent.profit
                    job_profit[1] += 1

                    jobs[agent.job] = job_profit

                profits = []
                for job in jobs:
                    profits.append((jobs[job][0]/jobs[job][1], job))

                profits.sort(key=lambda x: x[0], reverse=True)

                agents.append(Agent(jobs.by_name(profits[0][1]), self))

            self._agents = agents

        ## DEBUG
        for agent in self._agents:
            dump_agent(agent)

    def make_charts(self):
        # TODO: Decide if these will be general dependencies, or if charts will
        #       be an optional feature and thus these optional dependencies.
        import matplotlib.pyplot as plt
        import numpy as np

        hist = self.history()

        for good in goods.all():
            prices = []
            errs = [[],[]]
            volumes = []

            days = list(range(1,len(hist[good])+1))

            for trades in hist[good]:
                if trades.mean is not None:
                    prices.append(trades.mean)

                    errs[0].append(trades.mean - trades.low)
                    errs[1].append(trades.high - trades.mean)
                else:
                    prices.append(np.nan)

                    errs[0].append(np.nan)
                    errs[1].append(np.nan)

                volumes.append(trades.volume or 0)

            plt.figure()

            plt.suptitle('{}-Day History for {}'.format(days[-1], good))

            ax1 = plt.subplot(211)
            ax1.set_ylabel('Price')
            ax1.set_xlabel('Day')
            ax1.errorbar(days, prices, yerr=errs)

            ax2 = plt.subplot(212, sharex=ax1)
            ax2.set_ylabel('Volume')
            ax2.bar(days, volumes)

            plt.subplots_adjust(wspace=0, hspace=0)

            plt.savefig('{}.png'.format(good), bbox_inches='tight')
            plt.close()

    def history(self, depth=None):
        return self._history.history(depth)

    def aggregate(self, good, depth=None):
        return self._history.aggregate(good, depth)


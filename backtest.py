import pandas as pd
import matplotlib.pyplot as plt
from Strategy import SmaStrategy

class AccountInfo:

    def __init__(self, source, initial_capital, commission):
        self._source = source
        self._initial_capital = initial_capital
        self._commission = commission
        self._position = 0
        self._cash = initial_capital
        self._i = 0
        self._account = []
        self._time = []
        self._benchmark = []

    @property
    def initial_cash(self):
        return self._inital_cash

    @property
    def cash(self):
        return self._cash

    @property
    def position(self):
        return self._position

    @property
    def current_price(self):
        return self._source.Close[self._i]

    @property
    def market_value(self):
        return self._cash + self._position * self.current_price

    def buy(self):
        self._position = float(self._cash * (1 - self._commission) / self.current_price)
        self._cash = 0.0

    def sell(self):
        self._cash += float(self._position * self.current_price * (1 - self._commission))
        self._account.append(int(self._cash))
        self._time.append(self._source.index[self._i])
        # self._benchmark.append(self._initial_capital/self._source.Close[0] * self._source.Close[self._i])
        self._position = 0.0

    def next(self, tick):
        self._i = tick

class Backtest:
    def __init__(self, source, strategy_type, broker_type, initial_capital, commission):
        if not source.index.is_monotonic_increasing:
            source = source.sort_index()
        self._source = source
        self._broker = broker_type(source, initial_capital, commission)
        self._strategy = strategy_type(self._broker, self._source)

    def run(self):
        self._strategy.init()
        start = 2
        end = len(self._source)
        for i in range(start, end):
            self._broker.next(i)
            self._strategy.next(i)
        print(self._broker.market_value - self._broker._initial_capital)

        plt.plot(self._broker._time, self._broker._account,label="cash")
        # plt.plot(self._broker._time, self._broker._benchmark, label="benchmark")
        plt.legend()
        plt.show()

def main():
    BTCUSD = pd.read_csv('BTCUSD_1hr.csv', index_col=1,parse_dates=[1],infer_datetime_format=True)
    BTCUSD = BTCUSD.drop(columns=["Unix Timestamp"], axis=1)
    # BTCUSD = pd.read_csv('BTCUSD_1hr.csv', index_col=0, parse_dates=[0], infer_datetime_format=True)
    Backtest(BTCUSD, SmaStrategy, AccountInfo, 10000.0, 0).run()
if __name__ == '__main__':
    main()
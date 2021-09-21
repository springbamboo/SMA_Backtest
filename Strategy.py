import numpy as np
import pandas as pd

def SMA(series, term):
    return pd.Series(series).rolling(term).mean()

def crossover(series1, series2):
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]

class SmaStrategy():

    def __init__(self, broker, source):
        self._broker = broker
        self._source = source
        self._tick = 0

    def calulate_SMA(self, function, *args):
        return np.asarray(function(*args))

    @property
    def tick(self):
        return self._tick

    @property
    def source(self):
        return self._source

    def buy(self):
        self._broker.buy()

    def sell(self):
        self._broker.sell()

    fast = 41
    slow = 134

    def init(self):
        self.sma_fast = self.calulate_SMA(SMA, self.source.Close, self.fast)
        self.sma_slow = self.calulate_SMA(SMA, self.source.Close, self.slow)
    
    def next(self, tick):
        if crossover(self.sma_fast[:tick], self.sma_slow[:tick]):
            self.buy()
        elif crossover(self.sma_slow[:tick], self.sma_fast[:tick]):
            self.sell()
        else:
            pass




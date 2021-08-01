import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import logging

from datetime import datetime
from functools import reduce

from .market_data_provider import MarketDataProvider
from .watchlist import Watchlist
from summary.models import Trade

class MeanReversionTrader:
    TRADE_MARGIN = 0.05 # 5%
    CLOSE_MARGIN = 0.01 # 1%
    
    # Currently one either we have one stock or zero
    TRADE_QUANTITY = 1

    WATCHLIST = Watchlist.WATCHLIST

    def __init__(self):
        self.marketDataProvider = MarketDataProvider()
        self.logger = logging.getLogger('django')
        self.api = tradeapi.REST()

    def market_check(self):
        for symbol in self.WATCHLIST:
            self.assess(symbol)

    def assess(self, symbol, position=None, with_plots=False):

        times, prices = self.marketDataProvider.get_market_data(symbol)
        moving_average = self.moving_average(
            prices,
            self.marketDataProvider.WINDOW,
            self.marketDataProvider.WINDOW
        )
        prices = prices[self.marketDataProvider.WINDOW:]
        
        try:
            position = self.api.get_position(symbol)        
        except:
            # When there's no position an error is thrown by the api
            # but it just means we have no position open, we can go further
            pass

        actual_price = prices[-1]
        average_price = moving_average[-1]

        difference = average_price - actual_price
        difference_in_ratio = abs(float(difference)) / actual_price
        trade = None
        open_close = None

        if position:
            if position.side == 'short':
                if difference > 0 or difference_in_ratio < self.CLOSE_MARGIN:
                    trade = 'buy'
            else:
                if difference < 0 or difference_in_ratio < self.CLOSE_MARGIN:
                    trade = 'sell'

            if trade:
                open_close = 'close'
                try:
                    trade_object = Trade.objects.filter(stock=symbol, close_price=None, date_of_close=None)
                    trade_object = trade_object[0]
                    trade_object.date_of_close = datetime.now()
                    trade_object.close_price = round(actual_price, 3)
                    trade_object.save()
                except:
                    pass

        # There was no open position       
        else:
            if difference_in_ratio > self.TRADE_MARGIN:
                if difference < 0:
                    trade = 'sell'
                else:
                    trade = 'buy'
            
            if trade:
                open_close = 'open'
                trade_object = Trade.objects.create(
                    stock=symbol,
                    side=trade,
                    date_of_open=datetime.now(),
                    open_price=round(actual_price, 3),
                )

        if trade:
            self.api.submit_order(
                symbol=symbol,
                qty=self.TRADE_QUANTITY,
                side=trade,
                type='market',
                time_in_force='gtc'
            )
            self.log_trade(symbol, trade, actual_price, average_price)
            if with_plots:
                self.plot_at_trade(symbol, open_close, times, prices, moving_average)

    def moving_average(self, sequence: list, window: int, offset=0):      
        """
            Currently this method is more complicated than required.
            It is prepared to calculate different moving averages
            from the same data sequence.
            E.g. long/medium/short moving averages
        """        
        moving_average = []

        rolling = reduce((lambda x, y: x + y/window), sequence[offset - window:offset], 0)
        for x in range(offset, len(sequence)):
            rolling = rolling - (sequence[x-window] / window)
            rolling = rolling + (sequence[x] / window)
            moving_average.append(rolling)
        
        return moving_average

    def log_trade(self, symbol, trade, actual_price, average_price):
        self.logger = logging.getLogger('django')
        self.logger.info('### TRADE HAPPENED ###')
        self.logger.info(symbol)
        self.logger.info(trade)
        self.logger.info(f'actual price: ${round(actual_price, 3)}')
        self.logger.info(f'last moving average price: ${round(average_price, 3)}\n')

    def plot_at_trade(self, symbol, open_close, times, prices, moving_average):
        plt.plot(times, prices, label='real price')
        plt.plot(times, moving_average, label='moving average')
        plt.savefig(
            format='png',
            fname=f'{datetime.now().date()}_{datetime.now().hour}-{datetime.now().minute}_{symbol}_{open_close}.png'
        )
        plt.clf()

import alpaca_trade_api as tradeapi

class MarketDataProvider:

    # The point of having two windows is to be able to calculate
    # the first and subsequent moving averages (it needs at least WINDOW length data before itself)
    WINDOW = 20
    LIVE_WINDOW = 30
    TIME_FRAME = '1D'

    def __init__(self):
        self.api = tradeapi.REST()

    def get_market_data(self, symbol):

        barsets = self.api.get_barset(
            symbols=symbol,
            timeframe=self.TIME_FRAME,
            limit=self.LIVE_WINDOW + self.WINDOW,
        )

        bars = barsets[symbol]

        times = list(map(lambda bar: bar.t, bars))
        times = times[self.WINDOW:]
        prices = list(map(lambda bar: bar.c, bars))

        #bars = list(map(lambda bar: [bar.c, bar.t], bars))
        # print(symbol)
        # for _ in range(0, len(bars)):
        #     print(f'{_} price: {bars[_][0]} - date: {bars[_][1]}')

        return times, prices

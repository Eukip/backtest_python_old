from datetime import datetime


class SellCondition():

    async def calculate(self, main_time, candles, timeframe):

        main_time = int(main_time.timestamp())
        dict = {
            '1min': main_time - (main_time % 60) - 60,
            '5min': main_time - (main_time % 300) - 300,
            '15min': main_time - (main_time % 900) - 900,
            '30min': main_time - (main_time % 1800) - 1800,
            '1hour': main_time - (main_time % 3600) - 3600,
            '4hour': main_time - (main_time % 14400) - 14400,
            '1day': main_time - (main_time % 86400) - 86400,
        }
        candle = dict.get(timeframe)
        a = datetime.utcfromtimestamp(candle)
        try:
            k = candles.index(
                next(x for x in candles if x['time'] == a)
            )
        except StopIteration:
            return None

        return k

    async def RSI(self, indicator_data, i, overbought, main_candle, candles, **kwargs):

        k = await self.calculate(main_candle['time'], candles, kwargs['time'])
        if k is None:
            return
        previous = indicator_data[k - 1]
        if previous == None:
            return
        rsi = int(previous > overbought)
        return rsi

    async def MACD(self, indicator_data, i, main_candle, candles, **kwargs):

        k = await self.calculate(main_candle['time'], candles, kwargs['time'])

        if k is None:
            return
        if indicator_data['macd'][k - 1] == None or indicator_data['signal'][k - 1] == None:
            return
        macd = int(indicator_data['macd'][k - 1] < indicator_data['signal'][k - 1])
        return macd

    async def AROON(self, indicator_data, i, oversold, overbought, main_candle, candles, **kwargs):

        k = await self.calculate(main_candle['time'], candles, kwargs['time'])

        if k is None:
            return

        previous = indicator_data[k - 1]
        if previous[0] == None:
            return
        aroon = int(previous[0] <=oversold  and previous[1] >= overbought)
        return aroon

sell_condition = SellCondition()
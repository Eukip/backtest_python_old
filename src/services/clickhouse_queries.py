from datetime import datetime
import logging
import pandas as pd
from services.clickhouser_driver import SQLExecutor



async def insert_data_to_candle_data(pair: str, period: str, time: datetime,
                      open: int, close: int, low: int, high: int, **kwargs):

    date_time = pd.to_datetime(time, utc=True, unit='ms')
    data = [{

                    "tradingpair": pair,
                    "time": date_time,
                    "open": float(open),
                    "close": float(close),
                    "low": float(low),
                    "high": float(high),
                }]

    ret = await SQLExecutor.async_insert(
        """
        INSERT INTO candle_data_{period} (tradingpair, time, open, close, low, high) VALUES
        """.format(period=period), data
    )


    return ret


async def insert_data_to_candle_data_bulk(period, candles):
    data = []
    for candle in candles:
        data.append({
            "tradingpair": candle["pair"],
            "time": pd.to_datetime(candle["time"], utc=True, unit='ms'),
            "open": float(candle["open"]),
            "close": float(candle["close"]),
            "low": float(candle["low"]),
            "high": float(candle["high"]),
            "volume": float(candle["volume"]),
        })

    ret = await SQLExecutor.async_insert(
        """
        INSERT INTO candle_data_{period} (tradingpair, time, open, close, low, high, volume) VALUES
        """.format(period=period), data
    )

    return ret


async def get_data_from_candle_data(pair: str, period: str, datetime_from: datetime, datetime_to: datetime):
    return await SQLExecutor.async_execute(
        '''
            SELECT
                time,
                MIN (open) as open,
                MAX (close) as close,
                MIN (low) as low,
                MAX (high) as high,
                MAX (volume) as volume,
                MAX (trades) as trades
            FROM candle_data_{period}
            WHERE tradingpair='{pair}' and
            time >= '{datetime_from}' and
                time < '{datetime_to}'
            GROUP BY
                tradingpair, time
            ORDER BY time
        '''.format(
            pair=pair, period=period, datetime_from=datetime_from, datetime_to=datetime_to
        )
    )




async def insert_parquet_to_candle_data(pair: str, dict: dict, period: str):
    date_time = pd.to_datetime(dict['open_time'], utc=True, unit='ms')
    data = [{

                    "tradingpair": pair,
                    "time": dict['open_time'],
                    "open": dict['open'],
                    "close": dict['close'],
                    "low": dict['low'],
                    "high": dict['high'],
                    "volume": dict['volume'],
                    "trades": dict['number_of_trades']
                }]

    ret = await SQLExecutor.async_insert(
        """
        INSERT INTO candle_data_{period} (tradingpair, time, open, close, low, high, volume, trades) VALUES
        """.format(period=period), data
    )

    return ret

from typing import Literal
import asyncio
from os import environ

from services.clickhouser_driver import SQLExecutor



async def create_candle_data_table(interval: Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"]):



    await SQLExecutor.async_create('''
            CREATE TABLE IF NOT EXISTS candle_data_{interval} (
                tradingpair String,
                time        DateTime,
                open        Float32,
                close       Float32,
                low         Float32,
                high        Float32,
                volume      Float32,
                trades      Float32
            )
            ENGINE = ReplacingMergeTree()
            ORDER BY
                (tradingpair, time);
        '''.format(interval=interval))





async def drop_candle_data_table(interval: Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"]):
    await SQLExecutor.async_execute(
        'DROP TABLE IF EXISTS candle_data_{interval};'.format(interval=interval)
    )





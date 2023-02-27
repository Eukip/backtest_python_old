import re
from datetime import datetime
from typing import List
import json
import pandas as pd
from fastapi import HTTPException
from httpx import AsyncClient
from starlette import status

from schemas.coin import CoinHistoryOut, CoinHistoryOutList
from services.clickhouse_queries import insert_data_to_candle_data,  get_data_from_candle_data, insert_data_to_candle_data_bulk


class HistoryDataService:
    client = AsyncClient()

    @classmethod
    async def get_history_data(
            cls, pair: str, period: str, datetime_from: datetime, datetime_to: datetime
    ) -> List[CoinHistoryOut]:

        coin_history_list: List[CoinHistoryOut] = []

        for history in await get_data_from_candle_data(pair, period, datetime_from, datetime_to):
            coin_history_list.append(history)
        return coin_history_list


    @classmethod
    async def get_history_from_binance(cls,
                                       pair: str,
                                       period: str,
                                       datetime_from: datetime,
                                       datetime_to: datetime):

        """
        Структура ответа от api.binance
        [
            [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
            ]
        ]
        api принимает дату в миллисекундах для преобразование timestamp в них домнажаем на 1000
        информация с https://stackoverflow.com/questions/41635547/convert-python-datetime-to-timestamp-in-milliseconds

        """
        interval = None
        coin_history_list: List[CoinHistoryOut] = []
        pair = pair.upper().replace(' ' ,'').replace('-' ,'')

        response = await cls.client.get(
            url='https://cryptocandledata.com/api/trading_pairs',
            params={
                'exchange': 'binance'
            },
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        content = response.content.decode("utf-8")

        if len(re.findall(fr'{pair}', content)) == 0:
            allowed_pairs = response.json()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Trading pair {pair} not found in allowed pairs."
                                   f" Allowed pairs: {allowed_pairs['trading_pairs']}"
                                )

        interval = re.sub(r'(\d+\w)\w+', r'\1', period)

        resp = await cls.client.get(
            url='https://cryptocandledata.com/api/candles',
            params={
                'exchange' : 'binance',
                'tradingPair' : pair,
                'interval' : interval,
                'startDateTime' : int(datetime_from.timestamp( )),
                'endDateTime' : int(datetime_to.timestamp( ))
                    },
            timeout=50.0,
        )
        if resp.status_code != status.HTTP_200_OK:
            raise HTTPException(resp.status_code, resp.json())
        candle_data = resp.json()
        
        
        for content in candle_data['candles']:
            content['time'] = content.pop('timestamp')
            content['pair'] = pair

        await insert_data_to_candle_data_bulk(period, candle_data['candles'])

        return CoinHistoryOutList.parse_obj(candle_data['candles']).__root__



    @classmethod
    async def get_from_binance(cls,
                                       pair: str,
                                       period: str,
                                       datetime_from: datetime,
                                       datetime_to: datetime):

        interval = None
        coin_history_list: List[CoinHistoryOut] = []
        pair = pair.upper().replace(' ', '').replace('-', '')
        response = await cls.client.get(
            url='https://cryptocandledata.com/api/trading_pairs',
            params={
                'exchange': 'binance'
            },
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        content = response.content.decode("utf-8")

        if len(re.findall(fr'{pair}', content)) == 0:
            allowed_pairs = response.json()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Trading pair {pair} not found in allowed pairs."
                                       f" Allowed pairs: {allowed_pairs['trading_pairs']}"
                                )

        if re.search(r'm', period):
            interval = re.split(r'i', period)[0]
        if re.search(r'h', period):
            interval = re.split(r'o', period)[0]
        if re.search(r'd', period):
            interval = re.split(r'a', period)[0]

        resp = await cls.client.get(
            url='https://cryptocandledata.com/api/candles',
            params={
                'exchange': 'binance',
                'tradingPair': pair,
                'interval': interval,
                'startDateTime' : int(datetime_from.timestamp( )),
                'endDateTime' : int(datetime_to.timestamp( ))
            },
            timeout=50.0,
        )

        if resp.status_code != status.HTTP_200_OK:
            raise HTTPException(resp.status_code, resp.json())

        candle_data = resp.json()

        for content in candle_data['candles']:
            coin_history_list.append \
                (CoinHistoryOut(time=content['timestamp'],
                                open=content['open'],
                                close=content['close'],
                                low=content['low'],
                                high=content['high']
                                )
                 )

        return coin_history_list

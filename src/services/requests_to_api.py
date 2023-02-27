import json
import re

from fastapi import HTTPException
from httpx import AsyncClient
from starlette import status
from typing import Optional


class RequestsToApi:

    client = AsyncClient()

    async def getOrderPriceByOHLCV(self, json_candles,
                        priceMinusPerc: Optional[float] = None
                        ):

        response =  await self.client.post(
            url=f'http://web/api/getOrderPriceByOHLCV.php',
            data={'ohlcv': json_candles,
                    'priceMinusPerc': priceMinusPerc},
        )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def buildFullOhlcv(self,  indicator: str, json_candles):

        response = await self.client.post(
            url=f'http://web/api/{indicator}.php',
            data={'ohlcv': json_candles},
            timeout=50.0
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def convertOHLCVupdated(self, indicator: str,
                                  json_candles, newScale,
                                  fromScale: Optional[int] = None):

        response = await self.client.post(
            url=f'http://web/api/{indicator}.php',
            data={'ohlcv': json_candles,
                    'newScale' : newScale,
                    'fromScale' : fromScale},
            timeout=50.0
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def exponentialParam(self,
                               json_candles, exp_period,
                               offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/exponentialParam.php',
            data={'numArray': json_candles,
                    'period': exp_period,
                    'offset': offset
                  },
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()



    async def indicator_aroon(self,
                              json_candles, aroon_period, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/indicator_aroon.php',
            data={'ohlcv': json_candles,
                    'period': aroon_period},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def indicator_bbandsw(self,
                                json_candles, bbandsw_period,
                                multiplyer,
                                offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/indicator_bbandsw.php',
            data={'ohlcv': json_candles,
                    'period': bbandsw_period,
                    'multiplyer' : multiplyer,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()

    async def ohclv_bbandsB(self,
                            json_candles, bbandsb_period,
                            multiplyer,
                            offset: Optional[int] = None, **kwargs):
        response = await self.client.post(
            url=f'http://web/api/ohclv_bbandsB.php',
            data={'ohlcv': json_candles,
                  'period': bbandsb_period,
                  'multiplyer': multiplyer,
                  'offset': offset},
            timeout=50.0,
        )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def indicator_macd(self, json_candles,
                             periodFast, periodLong, periodSignal,
                             type: Optional[str] = 'percent',
                             offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/indicator_macd.php',
            data={'ohlcv': json_candles,
                    'periodFast': periodFast,
                    'periodLong': periodLong,
                    'periodSignal': periodSignal,
                    'type': type,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())


        normolize_resp = json.loads(response.text)
        return normolize_resp


    async def indicator_rsi(self,
                            json_candles, rsi_period,
                            offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/indicator_rsi.php',
            data={'ohlcv': json_candles,
                    'period': rsi_period,
                    'offset': offset},
            timeout=50.0,
        )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())


        normolize_resp = json.loads(response.text)


        return normolize_resp


    async def indicator_rsi_tv(self,
                               json_candles, rsi_tv_period,
                               offset: Optional[int] = None, **kwargs):
        response = await self.client.post(
            url=f'http://web/api/indicator_rsi_tv.php',
            data={'ohlcv': json_candles,
                    'period': rsi_tv_period,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def ohclv_bbands(self,
                           json_candles, bbands_period,
                           multiplyer,
                           offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/ohclv_bbands.php',
            data={'ohlcv': json_candles,
                    'period': bbands_period,
                    'multiplyer' : multiplyer,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def pumpProtectorLowperc(self, json_candles, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/pumpProtectorLowperc.php',
            data={'ohlcv': json_candles},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def rollingParam(self,
                          json_candles, rolling_param_period,
                          offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/rollingParam.php',
            data={'numArray': json_candles,
                    'period': rolling_param_period,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def simpleParam(self,
                          json_candles, simple_param_period,
                          offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/simpleParam.php',
            data={'numArray': json_candles,
                    'period': simple_param_period,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()

    async def smoothedParam(self,
                           json_candles, smoothed_param_period,
                           offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/smoothedParam.php',
            data={'numArray': json_candles,
                  'period': smoothed_param_period,
                  'offset': offset},
            timeout=50.0,
        )

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def waightedParam(self,
                           json_candles, waighted_param_period,
                           offset: Optional[int] = None, **kwargs):

        response = await self.client.post(
            url=f'http://web/api/waightedParam.php',
            data={'numArray': json_candles,
                  'period': waighted_param_period,
                  'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def standartDeviation(self, indicator: str,
                                json_candles, sma,
                                period, offset: Optional[int] = None):

        response = await self.client.post(
            url=f'http://web/api/{indicator}.php',
            data={'numarray': json_candles,
                    'sma' : sma,
                    'period': period,
                    'offset': offset},
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


    async def tradesToOHLCV(self, indicator, trades, time):

        response = await self.client.post(
            url=f'http://web/api/{indicator}.php',
            data={'trades': trades,
                    'time': time,
                    },
            timeout=50.0,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(response.status_code, response.json())

        return response.json()


requests_to_api = RequestsToApi()

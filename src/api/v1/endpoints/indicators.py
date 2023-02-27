import json
import os
from datetime import datetime, timedelta
from itertools import chain
from typing import Literal, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from starlette import status
from fastapi.responses import JSONResponse
from schemas.indicators import GetOrderPriceByOHLCV, BuildFullOhlcv, ConvertOHLCVUpdated
from services.currency import HistoryDataService
from services.json_datetime import json_datetime
from services.requests_to_api import requests_to_api
from services.two_d_array import create_two_d_array
from fastapi.responses import FileResponse

router = APIRouter()



class Status(BaseModel):
    status: bool


async def collect_data(trading_pair, timeframe, datetime_from, datetime_to, indicator_handler, ma_family=False, **params):
    data_candle = await HistoryDataService.get_history_data(
                                                            trading_pair,
                                                            timeframe,
                                                            datetime_from,
                                                            datetime_to,
                                                            )
    time_list = []
    json_candles = None
    if ma_family:
        json_candles = await json_datetime(data_candle)
    else:
        two_d_array = await create_two_d_array(data_candle)
        json_candles = await json_datetime(two_d_array)


    print("CALL indicator with params",indicator_handler, params)
    indicator_data = await indicator_handler(
                            json_candles,
                            **params)
    time_list = []
    i = 0
    for candle in data_candle:
        time_list.append({'time': candle['time'].isoformat()})
        if isinstance(indicator_data, dict):
            time_list[-1]['value'] = { k: indicator_data[k][i] for k in indicator_data.keys() }
        else:
            time_list[-1]['value'] =  indicator_data[i]
        i +=1

    return time_list
    


@router.get(
    "/indicators_json"
)
async def get_indicators_json():

    if not os.path.exists('/app/services/files/indicators.json'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"File indicators.json not found ")

    file = '/app/services/files/indicators.json'

    return FileResponse(file)




@router.get(
    "/rsi"
)
async def indicator_rsi(
        period: int = Query(14),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.indicator_rsi, rsi_period=period, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/ema"
)
async def exponential_param(
        period: int = Query(14),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from: datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0))
):
    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.exponentialParam, ma_family=True, exp_period=period, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/rma"
)
async def rolling_param(
        period: int = Query(14),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.rollingParam, ma_family=True, rolling_param_period=period, offset=offset)},
        status_code=status.HTTP_200_OK)



@router.get(
    "/sma"
)
async def simple_param(
        period: int = Query(14),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.simpleParam, ma_family=True, simple_param_period=period, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/smma"
)
async def smoothed_param(
        period: int = Query(14),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.smoothedParam, ma_family=True, smoothed_param_period=period, offset=offset)},
        status_code=status.HTTP_200_OK)



@router.get(
    "/wma"
)
async def waighted_param(
        period: int = Query(14),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.waightedParam, ma_family=True, waighted_param_period=period, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/aroon"
)
async def indicator_aroon(
        period: int = Query(14),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from: datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):
    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.indicator_aroon, aroon_period=period)},
        status_code=status.HTTP_200_OK)



@router.get(
    "/bbands"
)
async def ohclv_bbands(
        period: int = Query(14),
        multiplier: int = Query(1),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):
    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.ohclv_bbands, bbands_period=period, multiplyer=multiplier, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/bbandsw"
)
async def indicator_bbandsw(
        period: int = Query(14),
        multiplier: int = Query(1),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from: datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.indicator_bbandsw, bbandsw_period=period, multiplyer=multiplier, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/bbandsb"
)
async def indicator_bbandsB(
        period: int = Query(14),
        multiplier: int = Query(1),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from: datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.ohclv_bbandsB, bbandsb_period=period, multiplyer=multiplier, offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/macd"
)
async def indicator_macd(
        periodSignal: int = Query(9),
        periodFast: int = Query(12),
        periodLong: int = Query(26),
        offset: int = Query(1),
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.indicator_macd, periodFast=periodFast, periodLong=periodLong, periodSignal=periodSignal, type='percent', offset=offset)},
        status_code=status.HTTP_200_OK)


@router.get(
    "/rsi_tv"
)
async def indicator_rsi_tv(
        period: int = Query(1),
        offset: int = Query(1),
        trading_pair: str = Query('ETHBTC'),
        timeframe:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("1day"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):

    return JSONResponse(
        {"res": await collect_data(trading_pair, timeframe, datetime_from, datetime_to, requests_to_api.indicator_rsi_tv, rsi_tv_period=period,offset=offset)},
        status_code=status.HTTP_200_OK)



@router.get(
    "/pump_protector_low_perc"
)
async def pump_protector_low_perc(
        trading_pair: str = Query('VIDTBTC'),
        timeframe:  Literal["1day"] = Query("1day"),
        datetime_from:  datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):
    """Рассчет уровня максимальной цены ордера по дневному графику (1d-PumpProtect level)"""

    data_candle = await HistoryDataService.get_history_data(
                                                            trading_pair,
                                                            timeframe,
                                                            datetime_from,
                                                            datetime_to,
                                                            )
    two_d_array = await create_two_d_array(data_candle)

    json_candles = await json_datetime(two_d_array)

    indicator_data = await requests_to_api.pumpProtectorLowperc(
                                                               json_candles,
                                                                )

    if indicator_data == False:
        return Status(status=indicator_data)

    res = {}

    res['PumpProtectorLowPerc'] = indicator_data

    return JSONResponse(res, status_code=status.HTTP_200_OK)



@router.get(
    "/get_order_price_by_ohlcv",
    response_model=GetOrderPriceByOHLCV
)
async def get_order_price_by_ohlcv(
       priceMinusPerc: int = Query(10),
       trading_pair: str = Query('VIDTBTC'),
       timeframe: Literal["15min"] = Query(
           "15min"),
        datetime_from: datetime = Query(
            (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        datetime_to: datetime = Query(datetime.now().replace(microsecond=0))
):
    data_candle = await HistoryDataService.get_history_data(
                                                            trading_pair,
                                                            timeframe,
                                                            datetime_from,
                                                            datetime_to,
                                                            )
    two_d_array = await create_two_d_array(data_candle)

    json_candles = await json_datetime(two_d_array)


    indicator_data = await requests_to_api.getOrderPriceByOHLCV(
                                                                json_candles,
                                                                priceMinusPerc=priceMinusPerc
                                                                )
    return GetOrderPriceByOHLCV(price1=indicator_data[0],
                                price2=indicator_data[1],
                                level_info=indicator_data[2],
                                level=indicator_data[3])


# @router.get(
#     "/build_full_ohlcv"
# )
# async def build_full_ohlcv(
#        trading_pair: str = Query('ETHBTC'),
#         period: Literal["15min"] = Query(
#             "15min"),
#        datetime_from: datetime = Query(
#            (datetime.today() - timedelta(days=6)).replace(microsecond=0)),
#        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
# ):
#     full_ohlcv: List[BuildFullOhlcv] = []
#     data_candle = await HistoryDataService.get_history_data(
#                                                             trading_pair,
#                                                             period,
#                                                             datetime_from,
#                                                             datetime_to,
#                                                             )
#     two_d_array = await create_two_d_array(data_candle)
#
#     json_candles = await json_datetime(two_d_array)
#
#     indicator_data = await requests_to_api.buildFullOhlcv('buildFullOhlcv',
#                                                             json_candles
#                                                           )
#
#     for data in indicator_data:
#         full_ohlcv.append((BuildFullOhlcv(time=data[0], open=data[1],
#                           close=data[2], low=data[3],
#                           high=data[4], volume=data[5]))
#                           )
#
#     return full_ohlcv
#
#
#
#
#
#
# @router.get(
#     "/convert_ohlcv_updated"
# )
# async def convert_ohlcv_updated(
#         newScale: Literal["15m", "30m", "1h", "4h", "1D"] = Query("1D"),
#         fromScale: Literal[ "15m", "30m", "1h", "4h", "1D"] = Query("1m"),
#        trading_pair: str = Query('ETHBTC'),
#         period:  Literal["15min", "30min", "1hour", "4hours", "1day"] = Query("1day"),
#        datetime_from: datetime = Query(
#            (datetime.today() - timedelta(days=6)).replace(microsecond=0)),
#        datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
# ):
#     if newScale == fromScale:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='newScale and fromScale cant be equal')
#
#     converted_ohlcv: List[ConvertOHLCVUpdated] = []
#
#     data_candle = await HistoryDataService.get_history_data(
#                                                             trading_pair,
#                                                             period,
#                                                             datetime_from,
#                                                             datetime_to,
#                                                             )
#     two_d_array = await create_two_d_array(data_candle)
#
#     json_candles = await json_datetime(two_d_array)
#
#     indicator_data = await requests_to_api.convertOHLCVupdated('convertOHLCVupdated',
#                                                                json_candles,
#                                                                newScale,
#                                                                fromScale
#                                                                 )
#     for data in indicator_data:
#         if data[0] == 0:
#             data[0] = None
#         converted_ohlcv.append(ConvertOHLCVUpdated(time=data[0],
#                                                     open=data[1],
#                                                     close=data[2],
#                                                     low=data[3],
#                                                     high=data[4],
#                                                     volume=data[5]
#                                                    ))
#     return converted_ohlcv
#
#
#

#
# @router.get(
#     "/standart_deviation"
# )
# async def standart_deviation(
#         standart_deviation_period: int = Query(1),
#         sma_period: int = Query(1),
#         offset: int = Query(1),
#         sma_offset: int = Query(1),
#         trading_pair: str = Query('ETHBTC'),
#         period:  Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("1day"),
#         datetime_from: datetime = Query(
#            (datetime.today() - timedelta(days=6)).replace(microsecond=0)),
#         datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
# ):
#
#     data_candle = await HistoryDataService.get_history_data(
#                                                             trading_pair,
#                                                             period,
#                                                             datetime_from,
#                                                             datetime_to,
#                                                             )
#
#     close_array = []
#     for data in data_candle:
#         close_array.append(data['close'])
#
#     json_candles = await json_datetime(data_candle)
#
#     sma = await requests_to_api.rollingParam_or_simpleParam_or_smothedParam_or_waightedParam(
#                                                                'simpleParam',
#                                                                json_candles,
#                                                                period=sma_period,
#                                                                offset=sma_offset
#                                                                 )
#
#     json_sma = await json_datetime(sma)
#     json_close_array = await json_datetime(close_array)
#
#     indicator_data = await requests_to_api.standartDeviation(
#                                                                'standartDeviation',
#                                                                json_close_array,
#                                                                sma=json_sma,
#                                                                period=standart_deviation_period,
#                                                                offset=offset
#                                                             )
#
#     res = {}
#
#     res['standart_deviation'] = indicator_data
#
#     return JSONResponse(res, status_code=status.HTTP_200_OK)


# @router.get(
#     "/trades_to_ohlcv"
# )
# async def trades_to_ohlcv(
#         time:  Literal["1m", "15m"] = Query("15m"),
#         trading_pair: str = Query('VIDTBTC'),
#         period:  Literal["1min", "15min"] = Query("1day"),
#         datetime_from: datetime = Query(
#            (datetime.today() - timedelta(days=6)).replace(microsecond=0)),
#         datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
# ):
#
#
#     data_candle = await HistoryDataService.get_history_data(
#                                                             trading_pair,
#                                                             period,
#                                                             datetime_from,
#                                                             datetime_to,
#                                                             )
#
#     ############   ПОДУМАТЬ КАК ПОСЧИТАТЬ TRADES
#
#     #
#     # json_candles = await json_datetime(two_d_array)
#
#
#
#     trades = await create_two_d_array(data_candle)
#
#     indicator_data = await requests_to_api.tradesToOHLCV('tradesToOHLCV',
#                                                          trades=trades,
#                                                          time=time
#                                                          )
#     return indicator_data

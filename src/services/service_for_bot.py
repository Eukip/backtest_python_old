import time
from datetime import datetime
import collections
import json

from services.const import indicator_names
from services.currency import HistoryDataService
from services.infix_to_postfix import infixToPostfix
from services.json_datetime import json_datetime, DateTimeEncoder
from services.requests_to_api import requests_to_api
from services.two_d_array import create_two_d_array

async def adding_candles(data_candle: list, trading_pair, period):
    t = time.time()
    last_candle = data_candle[-50]

    extra_data_candle = list(await HistoryDataService.get_history_data(trading_pair, period,
                                                                       last_candle['time'],
                                                                       datetime.now().replace(microsecond=0)))

    print('adding_candles', time.time() - t)
    print('first_candle',  extra_data_candle[0])
    return extra_data_candle[:23000]



async def calculate_formula(formula, dict):

        for i, j in dict.items():
            formula = formula.replace(i,str(j))

        postfix_formula = await infixToPostfix(infix=formula)
        return postfix_formula






async def calculate_formula_indicators(indicators,
                                       trading_pair,
                                       datetime_from,
                                       datetime_to,
                                       i
                                       ):


    data = {}
    candles = {}

    for key in indicators.keys():
        params = indicators[key]
        indicator = indicator_names.values.get(params['indicator'], None)
        data_candle = await HistoryDataService.get_history_data(
                                                                trading_pair,
                                                                params['time'],
                                                                datetime_from,
                                                                datetime_to,
                                                            )

        two_d_array = await create_two_d_array(data_candle)
        json_candles = await json_datetime(two_d_array)
        indicator_data = await getattr(requests_to_api, indicator)(json_candles, **params)
        data[key] = indicator_data
        candles[params['time']] = data_candle

    return data, candles



async def condition(data: dict, deal_id, json_indicators, condition, i, candle, candles):
    formula_dict = {}
    data = data.get(deal_id)
    for key in data:
        indicator_data = data.get(key)
        params = json_indicators.get(key)
        params['candles'] = candles[deal_id][params['time']]
        params['main_candle'] = candle

        print(candle['time'], i)
        res = await getattr(condition, params['indicator'])(indicator_data, i, **params)
        formula_dict[key] = res

    return formula_dict



async def base_level_data_func(delta, data_candle, candle):
    correct_ohlcv = []
    for i in data_candle:
        if delta <= i['time'] <=candle['time']:
            correct_ohlcv.append(list(i.values()))
    data = json.dumps(correct_ohlcv,  cls=DateTimeEncoder)
    return data
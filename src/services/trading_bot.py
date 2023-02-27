import time
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse
from models import Deal
from models.pair import Pair
from models.order import Order, OrderStatus
from datetime import datetime, timedelta
from typing import Literal
from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from models.strategy import Strategy
from services.buy_condition import buy_condition
from services.currency import HistoryDataService
from services.requests_to_api import requests_to_api
from services.sell_condition import sell_condition
from services.service_for_bot import adding_candles, calculate_formula, calculate_formula_indicators, condition, \
     base_level_data_func


class Status(BaseModel):
    status: str


router = APIRouter()


async def main_trading_bot():

    q = time.time()
    strategy_id = 1
    trading_pair = 'VIDTBTC'
    market = 'Binance'
    balance = 100.0
    amount = 10
    deep = 25
    period = '15min'
    datetime_from = (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)
    datetime_to = (datetime(year=2020, month=10, day=25, hour=15)).replace(microsecond=0)

    strategy_orm = await Strategy.get_or_none(id=strategy_id)

    if strategy_orm == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Strategy with id {strategy_id} not found ")

    pair_orm = Pair(trading_pair=trading_pair, market=market)
    await pair_orm.save()

    deal_orm = await Deal.filter(strategy_id=strategy_id).all()

    if len(deal_orm) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Deals for strategy with id {strategy_id} not found ")

    data_candle = await HistoryDataService.get_history_data(
                                                            trading_pair,
                                                            period,
                                                            datetime_from,
                                                            datetime_to,
                                                        )
    i = 0

    outline_orders = []
    while len(data_candle) > 0:
        p = time.time()

        order_orms_to_db = []
        order_orms = []

        data, candles = {}, {}
        for deal in deal_orm:
            data_dict, candles_dict = await calculate_formula_indicators(deal.indicators, trading_pair, datetime_from,
                                                           datetime_to, i)
            data[deal.id] = data_dict
            candles[deal.id] = candles_dict

        for candle in data_candle:

            for deal in deal_orm:
                pr_delta = candle['time'] - timedelta(minutes=45)

                predict = [x for x in outline_orders if x.predicted_time.timestamp() == pr_delta.timestamp()]

                formula_dict = await condition(data, deal.id, deal.indicators, buy_condition, i, candle, candles)

                if None in formula_dict.values():
                    i += 1
                    continue

                ex_formula = await calculate_formula(deal.formula, formula_dict)

                if ex_formula :
                    delta = candle['time'] - timedelta(hours=12)
                    base_level_data = await base_level_data_func(delta, data_candle, candle)
                    base_level = await requests_to_api.getOrderPriceByOHLCV(base_level_data, deep)
                    order_orm = Order(base_price=float(base_level[0]),
                                      predicted_time=candle['time'],
                                      status=OrderStatus.pending
                                      )
                    outline_orders.append(order_orm)

                    #[x for x in outline_orders if x.status == OrderStatus.fail]

                    for order in predict:
                        if candle['low'] < float(order.base_price):
                            order.open_price = candle['open']
                            order.open_time = candle['time']
                            order.amount = amount
                            order.pair_id = pair_orm.id
                            order.deep = deep
                            order.deal_id = deal.id
                            order.deposit = balance - (order.open_price * order.amount)
                            order.status = OrderStatus.success

                            order_orms.append(order)

                            outline_orders.remove(order)
                            balance -= order.open_price * order.amount

                for order in order_orms:
                    formula_dict = await condition(data, deal.id, deal.indicators, sell_condition, i, candle, candles)

                    ex_formula = await calculate_formula(deal.formula, formula_dict)
                    if ex_formula:

                        order.close_price = candle['high']
                        balance += candle['high'] * order.amount
                        order.close_time = candle['time']
                        profit = (order.close_price - order.open_price) * order.amount
                        order_volume = amount * order.open_price
                        order.profit_cer_period =  (profit / order_volume) * 100
                        order.profit_to_deposit = (profit / order.deposit) * 100
                        order.absolute_profit = profit

                        order_orms_to_db.append(order)
                        order_orms.remove(order)

                i += 1

        data_candle = await adding_candles(data_candle, trading_pair, period)
        i = 0
        await Order.bulk_create(order_orms_to_db)

        print('BOOOOOOOOOOOOOOOOOOOOOOT', time.time() - q)

        if len(data_candle) == 50:
            print(balance, 'balance')
            return balance

    return balance


@router.post(
    "/trading_bot"
)
async def bot(background_tasks: BackgroundTasks):
    tasks = background_tasks.add_task(main_trading_bot)
    message = {'status': 'Start backtest'}
    return JSONResponse(message, background=tasks)
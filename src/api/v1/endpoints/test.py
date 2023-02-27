import json
from datetime import datetime, timedelta
from typing import List, Literal, Optional
from pydantic import BaseModel
from starlette import status
from models import Strategy, Order
from fastapi import APIRouter, Depends, Query, HTTPException

from schemas.order import TestPostOrder
from schemas.strategy import TestResultStrategyPydantic


class Status(BaseModel):
    status: str


router = APIRouter()


def parse_json():
    with open('orders.json') as file:
        data = json.load(file)
    return data['items']


@router.post('/populate_orders', response_model=Status)
async def orders_add_from_json():
    data = parse_json()

    for i in data:
        await Order.create(open_price=i['open_price'],
                          open_time=i['open_time'],
                          amount=i['amount'],
                          close_price=i['close_price'],
                          close_time=i['close_time'],
                          absolute_profit=i['absolute_profit'],
                          profit_cer_period=i['profit_cer_period'],
                          profit_to_deposit=i['profit_to_deposit'],
                           base=i['base'],
                           pair_id=i['pair_id'],
                           deep=i['deep']
                         )

    return Status(status=status.HTTP_200_OK)


@router.post('/test_create_strategy_results',
             response_model=TestResultStrategyPydantic
             )
async def create_strategy(
        strategy_id: int,
        count_orders: int = Query(5786),
        v_minus: int = Query(57),
        v_plus: int = Query(586),
        v_zero: int = Query(3000),
        not_closed: int = Query(20),
        profit: int = Query(78),

):
    strategy_orm = Strategy(
                            count_orders=count_orders,
                            v_zero=v_zero,
                            v_plus=v_plus,
                            v_minus=v_minus,
                            not_closed=not_closed,
                            profit=profit,
                            strategy_id=strategy_id
                            )

    await strategy_orm.save()

    return strategy_orm


@router.post('/test_create_order',
             response_model=TestPostOrder
             )
async def create_order(
        open_price: float = Query(5786),
        close_price: float = Query(5786),
        open_time: datetime = Query(
           (datetime(year=2020, month=10, day=9, hour=14)).replace(microsecond=0)),
        close_time: datetime = Query(
           (datetime(year=2020, month=10, day=15, hour=14)).replace(microsecond=0)),
        absolute_profit: int = Query(586),
        amount: float = Query(10),
        profit_cer_period: int = Query(20),
        profit_to_deposit: int = Query(78),
        deep: float = Query(10),
        base: str = Query(''),
        pair_id: int = Query(1)
):
    order_orm = Order(open_price=open_price,
                      open_time=open_time,
                      close_price=close_price,
                      close_time=close_time,
                      amount=amount,
                      pair_id=pair_id,
                      is_active=True,
                      absolute_profit=absolute_profit,
                      profit_cer_period=profit_cer_period,
                      profit_to_deposit=profit_to_deposit,
                      deep=deep,
                      base=base
                      )

    await order_orm.save()

    return order_orm


@router.delete('/delete_order_or_res_strategy',
               )
async def delete_order_or_res_strategy(
        order_id: Optional[int] = None,
        res_strategy_id: Optional[int] = None
):
    if order_id:
        order_orm = await Order.get_or_none(id=order_id)
        if order_orm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found order')
        await order_orm.delete()

    if res_strategy_id:
        res_strategy_orm = await Strategy.get_or_none(id=res_strategy_id)
        if res_strategy_orm is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found res strategy')
        await res_strategy_orm.delete()

    return Status(status='deleted')
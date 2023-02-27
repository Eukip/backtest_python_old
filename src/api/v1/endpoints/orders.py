import json

from pydantic import BaseModel
from starlette import status
from tortoise import Tortoise
from models.order import Order
from datetime import datetime, timedelta
from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from models.timeinterval import TimeInterval
from schemas.order import GetAllOrders, GetOrder
from fastapi_pagination import Page,  Params
from fastapi_pagination.ext.tortoise import paginate
from tortoise.expressions import F



router = APIRouter()


@router.get('/orders',
            response_model=Page[GetAllOrders]
            )
async def get_orders(
    time_interval: Optional[int] = None,
    opens: Optional[int] = None,
    profit_from: Optional[int] = None,
    profit_to: Optional[int] = None,
    dealprofit_from: Optional[float] = None,
    dealprofit_to: Optional[float] = None,
    depozprofit_from: Optional[float] = None,
    depozprofit_to: Optional[float] = None,
    open_price: Optional[float] = None,
    close_price: Optional[float] = None,
    time_in_order: Optional[str] = Query(
        default=None,
        title='Time in order filter',
        description='Работает, отправлять в формате DD-HH-MM "13-13-13"'
        ),
    order_status: Optional[str] = Query(
        default=None,
        title='Filtering with order status',
        description='Getting only two values for status: "Open" or "Close"'
    ),
    trading_pair: Optional[str] = None,
    deep_1: Optional[float] = None,
    deep_2: Optional[float] = None,
    deep_3: Optional[float] = None,
    strategy_id: Optional[int] = None,
    params: Params = Depends(),
):

    # print(sql)
    # print(datetime.today() - datetime(2022, 7, 9, 14, 0, 0, 0)) # 2 days, 16:32:14.376343
    # print(type(datetime.today() - datetime(2022, 7, 9, 14, 0, 0, 0))) # <class 'datetime.timedelta'>
    # 2020-10-09T14:00:00+00:00
    # a = await Order.get(id=1).values_list()
    # date_to_split = str(a[5])
    # print(date_to_split)
    # splited_list = date_to_split.split("+")
    # print(splited_list[0])
    # date_in_new_format = datetime.strptime(splited_list[0], "%y-%m-%d %H:%M:%S")
    # print(type(date_in_new_format))
    # datetime.strptime((('close_time').split("+"))[0],"%y-%m-%dT%H:%M:%S") - datetime.strptime(('open_time').split("+")[0],"%y-%m-%dT%H:%M:%S")
    orders_qs = Order.all().prefetch_related('pair', 'deal').all()

    if strategy_id:
        orders_qs = Order.filter(deal__strategy__id=strategy_id).distinct()
        print(orders_qs.sql())


    if time_in_order: # DD-HH-MM, ["DD-HH-MM"]
        days = time_in_order[:2]
        t_days = datetime.strptime(days, "%d")
        t_remain = datetime.strptime(time_in_order[3:],"%H-%M")
        delta = timedelta(days=t_days.day, hours=t_remain.hour, minutes=t_remain.minute)
        orders_qs = Order.filter(seconds_in_order__lte=delta.seconds).distinct()

        

    if time_interval:
        await check_exists_time_interval(time_interval)
        values = await TimeInterval.filter(id=time_interval).first().values_list()
        orders_qs = Order.filter(open_time__gte=values[1]).filter(close_time__lte=values[2])

    if opens:
        orders_qs = Order.filter(close_price=None).distinct()

    if profit_from and profit_to:
        orders_qs = Order.filter(absolute_profit__gte=profit_from).filter(absolute_profit__lte=profit_to).distinct()

    if dealprofit_from and dealprofit_to:
        orders_qs = Order.filter(profit_cer_period__gte=dealprofit_from).filter(profit_cer_period__lte=dealprofit_to).distinct()
    
    if depozprofit_from and depozprofit_to:
        orders_qs = Order.filter(profit_to_deposit__gte=depozprofit_from).filter(profit_to_deposit__lte=depozprofit_to).distinct()

    if order_status == "Open":
        orders_qs = Order.filter(close_time__isnull=True).distinct()

    if order_status == "Close":
        orders_qs = Order.filter(close_time__isnull=False).distinct()
    
    if open_price and close_price:
        orders_qs = Order.filter(open_price__gte=open_price,
                                 close_price__lte=close_price).distinct()

    if trading_pair:
        orders_qs = Order.filter(pair__trading_pair__icontains=trading_pair).distinct()

    if deep_1:
        orders_qs = Order.filter(deep=deep_1).distinct()
    
    if deep_2:
        orders_qs = Order.filter(deep=deep_2).distinct()
    
    if deep_3:
        orders_qs = Order.filter(deep=deep_3).distinct()

    return await paginate(orders_qs, params)




@router.get('/{order_id}',
            response_model=GetOrder
            )
async def get_orders(
    order_id: int
):
    await check_exists(order_id)

    order_orm = await Order.get_or_none(id=order_id).prefetch_related('pair',
                                                                      'deal__strategy')

    print(order_orm.__dict__)

    return order_orm



async def check_exists(order_id: int):
    if not await Order.exists(id=order_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order with id {order_id} not found ")


async def check_exists_time_interval(interval_id: int):
    if not await TimeInterval.exists(id=interval_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"TimeInterval with id {interval_id} not found ")

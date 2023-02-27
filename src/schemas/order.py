from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel

class PairPydantic(PydanticModel):
    id: int
    trading_pair: str
    market: str

class StrategyPydantic(PydanticModel):
    id: int
    name: str
    formula: str


class GetAllOrders(PydanticModel):
    id: int
    open_price: float
    open_time: datetime
    amount: float
    close_price: Optional[float]
    close_time: datetime
    absolute_profit: Optional[int]
    profit_cer_period: Optional[int]
    profit_to_deposit: Optional[int]
    base: Optional[str]
    time_in_order: Optional[timedelta]
    pair: PairPydantic

    class Config:
        orm_mode = True

class GetOrder(PydanticModel):
    id: int
    open_price: float
    open_time: datetime
    amount: float
    close_price: float
    close_time: datetime
    time_in_order: Optional[timedelta]
    pair: PairPydantic


class TestPostOrder(PydanticModel):
    id: int
    open_price: float
    open_time: datetime
    amount: float
    close_price: float
    close_time: datetime
    absolute_profit: int
    profit_cer_period: int
    profit_to_deposit: int
    deep: float
    base: str

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel



class Deal(PydanticModel):
    id: int
    formula: str
    indicators: dict








class RequestStrategy(PydanticModel):
    id: int
    name: Optional[str]
    master_id: Optional[int]
    base: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]
    deal_depth: Optional[float]
    png_from_xmind_input: Optional[str]
    png_from_xmind_output: Optional[str]
    self_strategy: Optional[int]


class StrategyPydantic(PydanticModel):
    id: int
    count_orders: Optional[int]
    v_minus: Optional[int]
    v_plus: Optional[int]
    v_zero: Optional[int]
    not_closed: Optional[int]
    absolute_profit: Optional[float]
    profit_cer_period: Optional[float]
    profit_to_deposit: Optional[float]
    self_master_id: Optional[int]

    class Config:
        orm_mode = True

class TestResultStrategyPydantic(PydanticModel):
    id: int
    count_orders: int
    v_minus: int
    v_plus: int
    v_zero: int
    not_closed: int
    profit: int


class StrategiesPydantic(PydanticModel):

    id: Optional[int]
    name: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]

    count_orders: Optional[int]
    v_minus: Optional[int]
    v_plus: Optional[int]
    v_zero: Optional[int]
    not_closed: Optional[int]

    profit_cer_period: Optional[float]
    profit_to_deposit: Optional[float]
    absolute_profit: Optional[float]

    png_from_xmind_input: Optional[str]
    png_from_xmind_output: Optional[str]

    base: Optional[str]

    moment_max_drawdown: Optional[str]
    all_order_max_drawdown: Optional[str]

    self_master_id: Optional[int]
    archived: Optional[bool]

    deal_depth: Optional[float]

    deal: Optional[List[Deal]]





class CreateResponseStrategiesPydantic(PydanticModel):
    id: Optional[int]
    name: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]

    count_orders: Optional[int]
    v_minus: Optional[int]
    v_plus: Optional[int]
    v_zero: Optional[int]
    not_closed: Optional[int]

    profit_cer_period: Optional[float]
    profit_to_deposit: Optional[float]
    absolute_profit: Optional[float]

    png_from_xmind_input: Optional[str]
    png_from_xmind_output: Optional[str]

    base: Optional[str]

    moment_max_drawdown: Optional[str]
    all_order_max_drawdown: Optional[str]

    deal_depth: Optional[float]

    class Config:
        orm_mode = True



class CreateRequestStrategiesPydantic(BaseModel):

    name: Optional[str]
    self_master_id: Optional[int]

    base: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]

    deal_depth_1: Optional[float]
    deal_depth_2: Optional[float]
    deal_depth_3: Optional[float]
    
    deposit_limit: Optional[int]








class AdminStrategiesPydantic(PydanticModel):
    id: int
    name: Optional[str]
    base: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]
    deal_depth: Optional[float]
    profit_to_deal: Optional[float]
    profit_to_depoz: Optional[float]
    absolute_profit: Optional[float]
    self_master_id: Optional[int]








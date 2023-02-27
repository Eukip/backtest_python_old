from typing import List, Optional, Any

from pydantic import BaseModel, Json
from tortoise.contrib.pydantic import PydanticModel


class StrategyRequest(PydanticModel):
    id: Optional[int]
    name: Optional[str]
    base: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]
    deal_depth: Optional[float]

class DealRequest(BaseModel):
    formula: str
    indicators: dict




class DealRequestPydantic(PydanticModel):
    deal: Optional[DealRequest]
    strategy: Optional[StrategyRequest]





class StrategyResponse(PydanticModel):
    id: int
    name: str
    base: Optional[str]
    daily_turnover_from: Optional[int]
    daily_turnover_to: Optional[int]
    deal_depth: Optional[float]

class DealResponse(PydanticModel):
    id: int
    formula: str
    indicators: dict

class DealResponsePydantic(PydanticModel):
    deal: DealResponse
    strategy: StrategyResponse



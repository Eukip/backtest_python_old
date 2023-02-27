from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel


class GetOrderPriceByOHLCV(BaseModel):
    price1: float
    price2: float
    level_info: str
    level: int



class BuildFullOhlcv(BaseModel):
    time: datetime
    open: Optional[float]
    close: Optional[float]
    low: Optional[float]
    high: Optional[float]
    volume: Optional[float]


class ConvertOHLCVUpdated(BaseModel):
    time: Optional[datetime]
    open: Optional[float]
    close: Optional[float]
    low: Optional[float]
    high: Optional[float]
    volume: Optional[float]

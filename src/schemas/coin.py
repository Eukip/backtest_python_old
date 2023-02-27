from datetime import datetime
from typing import List, Optional

# from pycommon import BaseMoney, Money
from pydantic import BaseModel


class CoinHistoryOut(BaseModel):#BaseMoney
    time: datetime
    open: Optional[float]
    close: Optional[float]
    low: Optional[float]
    high: Optional[float]


class CoinHistoryOutList(BaseModel):
    __root__: List[CoinHistoryOut]


class GetClickHouseData(BaseModel):#BaseMoney
    time: datetime
    open: Optional[float]
    close: Optional[float]
    low: Optional[float]
    high: Optional[float]
    volume: Optional[float]
    trades: Optional[float]

from datetime import datetime
from typing import List, Optional

from tortoise.contrib.pydantic import PydanticModel


class ResponseCreateMasterTimeInterval(PydanticModel):
    id: int
    name: str


class TimeInterval(PydanticModel):
    id: int
    datetime_from: Optional[datetime]
    datetime_to: Optional[datetime]


class ResponseTimeInterval(PydanticModel):
    id: int
    datetime_from: datetime
    datetime_to: datetime
    master_time_id: Optional[int]


class GetMasterTimeInterval(PydanticModel):
    id: Optional[int]
    name: Optional[str]
    timeinterval: Optional[List[TimeInterval]]


class RequestTimeInterval(PydanticModel):
    datetime_from: Optional[datetime]
    datetime_to: Optional[datetime]

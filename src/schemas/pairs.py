from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel


class PairResponse(PydanticModel):
    id: int
    market: str
    trading_pair: str

from typing import List, Optional, Any

from pydantic import BaseModel, Json
from tortoise.contrib.pydantic import PydanticModel


class FormulaRequest(PydanticModel):
    id: Optional[int]
    name: Optional[str]
    formula: Optional[str]
    deal: Optional[int]

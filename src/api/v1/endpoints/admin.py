from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from models import Strategy
from schemas.strategy import AdminStrategiesPydantic

router = APIRouter()


class Status(BaseModel):
    status: bool


@router.post('/strategy',
             response_model=AdminStrategiesPydantic
             )
async def create_strategy(
        name: Optional[str],
        base: Optional[str],
        daily_turnover_from: Optional[int],
        daily_turnover_to: Optional[int],
        deal_depth_1: Optional[float],
        deal_depth_2: Optional[float],
        deal_depth_3: Optional[float],
        deposit_limit: Optional[int],
        master_id: Optional[int]
):
    strategy_orm = await Strategy.create(name=name,
                                         base=base,
                                         daily_turnover_from=daily_turnover_from,
                                         daily_turnover_to=daily_turnover_to,
                                         deal_depth_1=deal_depth_1,
                                         deal_depth_2=deal_depth_2,
                                         deal_depth_3=deal_depth_3,
                                         deposit_limit=deposit_limit,
                                         self_master_id=master_id)
    return strategy_orm
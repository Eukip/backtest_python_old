from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel
from starlette import status
from models import TimeInterval, MasterTimeInterval
from schemas.timeinterval import ResponseTimeInterval, RequestTimeInterval, ResponseCreateMasterTimeInterval, GetMasterTimeInterval


router = APIRouter()


class Status(BaseModel):
    status: str


@router.post('/master_timeinterval/create_master_timeinterval',
             response_model=ResponseCreateMasterTimeInterval
             )
async def create_master_timeinterval(
    name: str,

):
    timeinterval_orm = MasterTimeInterval(name=name)
    await timeinterval_orm.save()

    return timeinterval_orm


@router.post('/create_timeinterval',
             response_model=ResponseTimeInterval
             )
async def create_timeinterval(
    master_time_id: int,
    datetime_from: datetime = Query(
           (datetime.today() - timedelta(days=6)).replace(microsecond=0)),
    datetime_to: datetime = Query(datetime.now().replace(microsecond=0)),
):
    master_orm = MasterTimeInterval.get_or_none(id=master_time_id)
    if master_orm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MasterTimeInterval with id {master_time_id} not found ")

    timeinterval_orm = TimeInterval(
                            datetime_from=datetime_from,
                            datetime_to=datetime_to,
                            master_time_id=master_time_id
                            )
    await timeinterval_orm.save()

    return timeinterval_orm


@router.get('/{timeinterval_id}',
            response_model=ResponseTimeInterval)
async def get_timeinterval(timeinterval_id: int
):
    await check_exists(timeinterval_id)

    timeinterval_orm = await TimeInterval.get(id=timeinterval_id)

    return timeinterval_orm


@router.get('/master_timeinterval/{master_timeinterval_id}',
            response_model=GetMasterTimeInterval)
async def get_master_timeinterval(master_timeinterval_id: int):
    
    master_orm = await MasterTimeInterval.get_or_none(id=master_timeinterval_id).prefetch_related('timeinterval')
    if master_orm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MasterTimeInterval with id {master_timeinterval_id} not found ")

    return master_orm


@router.delete('/master_timeinterval/{master_timeinterval_id}'
            )
async def delete_master_timeinterval(master_timeinterval_id: int
):
    master_orm = await MasterTimeInterval.get_or_none(id=master_timeinterval_id)
    if master_orm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MasterTimeInterval with id {master_timeinterval_id} not found ")


    await master_orm.delete()

    return Status(status=f'MasterTimeInterval with id {master_timeinterval_id} deleted')



@router.delete('/{timeinterval_id}'
            )
async def delete_timeinterval(timeinterval_id: int
):
    await check_exists(timeinterval_id)

    timeinterval_orm = await TimeInterval.get(id=timeinterval_id)
    await timeinterval_orm.delete()

    return Status(status=f'Timeinterval with id {timeinterval_id} deleted')



@router.get('',
            response_model=List[GetMasterTimeInterval],
            )
async def get_all_master_timeinterval():

    master_orm = await MasterTimeInterval.all().prefetch_related('timeinterval')

    return master_orm


@router.put('/update_timeinterval',
            response_model=ResponseTimeInterval
            )
async def update_timeinterval(
    timeinterval_id: int,
    timeinterval: RequestTimeInterval
):
    await check_exists(timeinterval_id)
    update_dict = timeinterval.dict(exclude_unset=True)

    await TimeInterval.filter(id=timeinterval_id).update(**update_dict)
    timeinterval_orm = await TimeInterval.get_or_none(id=timeinterval_id)

    return timeinterval_orm



@router.put('/master_timeinterval/update_master_timeinterval',
            response_model=GetMasterTimeInterval
            )
async def update_master_timeinterval(master_interval_id: int, name: str
):

    master_orm = await MasterTimeInterval.get_or_none(id=master_interval_id).prefetch_related('timeinterval')
    if master_orm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MasterTimeInterval with id {master_interval_id} not found ")
    master_orm.name = name
    await master_orm.save()

    return master_orm


async def check_exists(timeinterval_id: int):
    if not await TimeInterval.exists(id=timeinterval_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"TimeInterval with id {timeinterval_id} not found ")

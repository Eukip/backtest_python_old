
from pydantic import BaseModel
from starlette import status
from models.pair import Pair
from datetime import datetime, timedelta
from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination import LimitOffsetPage, Page,  Params
from fastapi_pagination.ext.tortoise import paginate
from schemas.pairs import PairResponse


class Status(BaseModel):
    status: str


router = APIRouter()


@router.get('/get_all_pairs',
            response_model=Page[PairResponse]
            )
async def get_all_pairs(params: Params = Depends(),
    market: str = Query('Binance'),
):
    return await paginate(Pair.filter(market=market).all(), params)


@router.delete('/delete_pair/{pair_id}'
            )
async def delete_pair(pair_id: int):
    await check_exists(pair_id)
    pair_orm = await Pair.get(id=pair_id)
    pair = pair_orm.trading_pair
    await pair_orm.delete()
    return Status(status=f'Strategy with name {pair} deleted')




async def check_exists(id: int):
    if not await Pair.exists(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pair with id {id} not found ")
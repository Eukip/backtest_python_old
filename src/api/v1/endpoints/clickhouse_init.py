from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from services.clickhouse_db_fill import fill_clickhouse_table
from services.clickhouse_utils import create_candle_data_table, drop_candle_data_table


router = APIRouter()

class Status(BaseModel):
    status: str


@router.post(
    "/create_clickhouse_table",
    response_model=Status
)
async def create_clickhouse_table(interval: Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"]):

    await create_candle_data_table(interval)

    return Status(status=status.HTTP_200_OK)


@router.delete(
    "/drop_clickhouse_table",
    response_model=Status
)
async def create_clickhouse_table(interval: Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"]):

    await drop_candle_data_table(interval)

    return Status(status=status.HTTP_200_OK)


@router.post(
    "/fill_clickhouse_table"
)
async def fill_clickhouse(background_tasks: BackgroundTasks):
    tasks = background_tasks.add_task(fill_clickhouse_table)
    return JSONResponse(status.HTTP_200_OK, background=tasks)



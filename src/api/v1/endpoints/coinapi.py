from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi import APIRouter
from pydantic import BaseModel
from services.load_minute_canldes_coinapi import load_canldes_by_symbol_id
from services.parse_insert_exchanges_symbols_coinapi import load_exchanges, load_symbols
from tortoise import Tortoise



router = APIRouter()


class Status(BaseModel):
    status: str


@router.post(
    "/load_candles_by_symbol_id"
)
async def load_candles_by_symbol_id(
    # background_tasks: BackgroundTasks,
    symbol_id: int):
    # tasks = background_tasks.add_task(load_canldes_by_symbol_id(symbol_id))
    return JSONResponse(
        status.HTTP_200_OK, 
        content=load_canldes_by_symbol_id(symbol_id), 
        # background=tasks
    )


@router.post(
    "/load_exchanges"
)
async def exchanges(background_tasks: BackgroundTasks):
    #tasks = background_tasks.add_task(load_exchanges)
    await load_exchanges()
    return JSONResponse(
        status.HTTP_200_OK,
        #background=tasks
    )


@router.post(
    "/load_symbols"
)
async def symbols(background_tasks: BackgroundTasks):
    #tasks = background_tasks.add_task(load_symbols)
    await load_symbols()
    return JSONResponse(
        status.HTTP_200_OK,
        #background=tasks
    )


@router.get(
    "/check_exchange"
)
async def get_exchange():
    conn = Tortoise.get_connection('default')
    exchange_orm = await conn.execute_query(
        'SELECT * FROM "exchange"'
    )
    return exchange_orm


@router.get(
    "/check_symbols"
)
async def get_symbols():
    conn = Tortoise.get_connection('default')
    symbols_orm = await conn.execute_query(
        'SELECT * FROM "symbols"'
    )
    return symbols_orm

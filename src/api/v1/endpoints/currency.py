from datetime import datetime, timedelta
from typing import List, Literal, Optional



from fastapi import APIRouter, Depends, Query
from services.clickhouser_driver import SQLExecutor
from services.currency import HistoryDataService
from schemas.coin import CoinHistoryOut, GetClickHouseData

router = APIRouter()


@router.get('/history_binance', response_model=List[CoinHistoryOut])
async def coin_history_graph(
    pair: str,
    period: Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("1day"),
    datetime_from: datetime = Query((datetime.today() - timedelta(days=1)).replace(microsecond = 0)),
    datetime_to: datetime = Query(datetime.now().replace(microsecond = 0)),
    history_data: HistoryDataService = Depends(),
):
    return await history_data.get_history_from_binance(
        pair,
        period,
        datetime_from,
        datetime_to,
    )



@router.get('/clickhouse_data', response_model=List[GetClickHouseData])
async def coin_history_graph(
    datetime_from: Optional[datetime] = Query(default=None),
    datetime_to: Optional[datetime] = Query(default=None),
    pair: str = Query('VIDTBTC'),
    period: Literal["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"] = Query("15min"),
    history_data: HistoryDataService = Depends(),
):
    if datetime_from is None and datetime_to is None:
        return await SQLExecutor.async_execute(
            f"""
            SELECT time,open,close,low,high,volume,trades  FROM candle_data_{period}
            WHERE tradingpair='{pair}'
            ORDER BY time desc
            LIMIT 1
            """
        )
    return await history_data.get_history_data(
        pair,
        period,
        datetime_from,
        datetime_to,
    )

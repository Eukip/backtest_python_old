from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from models import Strategy, Deal
from schemas.deal import DealRequestPydantic, DealResponsePydantic


router = APIRouter()


class Status(BaseModel):
    status: bool


@router.post('/create_strategy_and_deal',
             response_model=DealResponsePydantic
             )
async def create_strategy_and_deal(params: DealRequestPydantic):

    if params.strategy.id is not None:
        strategy_orm = await Strategy.get(id=params.strategy.id)
    else:
        strategy_orm = Strategy(name=params.strategy.name,
                                base=params.strategy.base,
                                daily_turnover_from=params.strategy.daily_turnover_from,
                                daily_turnover_to=params.strategy.daily_turnover_to,
                                deal_depth=params.strategy.deal_depth,
                                master_id=params.master_id
                                )
        await strategy_orm.save()

    deal_orm = Deal(formula=params.deal.formula,
                    indicators=params.deal.indicators,
                    strategy_id=strategy_orm.id)
    await deal_orm.save()

    return DealResponsePydantic(deal=deal_orm, strategy=strategy_orm)

# HOW TO REQUEST IN METHOD
# {
#    "deal":{
#       "formula":"(1&2)",
#       "indicators":{
#          "1":{
#             "time":"1min",
#             "oversold":30,
#             "indicator":"RSI",
#             "overbought":70,
#             "rsi_period":15
#          },
#          "2":{
#             "time":"1min",
#             "indicator":"MACD",
#             "periodFast":12,
#             "periodLong":26,
#             "periodSignal":9
#          },
#          "3":{
#             "time":"1min",
#             "oversold":30,
#             "indicator":"AROON",
#             "overbought":70,
#             "aroon_period":15
#          }
#       }
#    },
#    "strategy": {
#     "name": "testy",
#     "base": "BTC",
#     "daily_turnover_from": 2,
#     "daily_turnover_to": 10,
#     "deal_depth": 3
#   },
#    "master_id":1
# }
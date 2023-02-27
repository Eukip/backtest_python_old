from fastapi import APIRouter

from api.v1.endpoints import currency, timeinterval, user, clickhouse_init, \
    orders, indicators, strategy, pairs, test, deal, admin, \
    coinapi
from services import trading_bot

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(currency.router, prefix="/currency", tags=["Currency"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(clickhouse_init.router, prefix="/clickhouse", tags=["Clickhouse"])
api_router.include_router(trading_bot.router, prefix="/bot", tags=["Bot"])
api_router.include_router(orders.router, prefix="/order", tags=["Order"])
api_router.include_router(indicators.router, prefix="/indicator", tags=["Indicator"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["Strategy"])
api_router.include_router(pairs.router, prefix="/pairs", tags=["Pairs"])
api_router.include_router(timeinterval.router, prefix="/timeinterval", tags=["TimeInterval"])
api_router.include_router(test.router, prefix="/test", tags=["Test"])
api_router.include_router(deal.router, prefix="/deal", tags=["Deal"])
api_router.include_router(coinapi.router, prefix="/coinapi", tags=["Coinapi"])

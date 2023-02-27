from urllib import request
from models import Symbols
import requests
from datetime import datetime, timedelta
from services.clickhouser_driver import SQLExecutor


OLD_API_KEY = 'AD143E2D-E5B8-4ECF-B292-06AA2E84AD3A'
NEW_API_KEY = 'C139C5E8-5C97-4A74-91AE-D6C08BF09E7D'


async def load_canldes_by_symbol_id(symbol_id: int):

    needed_symbol = await Symbols.get(id=symbol_id)
    date_start = needed_symbol.data_quote_start
    date_end = needed_symbol.data_quote_end
    request_symbol_id = needed_symbol.symbol_id
    trading_pair = needed_symbol.asset_id_base + needed_symbol.asset_id_quote
    
    date_end_while = datetime.strptime(date_start, "%Y-%m-%dT%H%M%S.%f") + timedelta(seconds=60000)
    data = []
    while date_end_while <= date_end:
        response = requests.get(
            url=f"https://rest.coinapi.io/v1/ohlcv/{request_symbol_id}/history?period_id=1MIN&time_start={date_start}&time_end={date_end_while}",
            headers={
                'X-CoinAPI-Key': OLD_API_KEY,
            }
        )

        candles = response.json()        

        
        for candle in candles:
            broken = None
            delta_time = datetime.strptime(candle['time_close'], "%Y-%m-%dT%H%M%S.%f") - datetime.strptime(candle['time_open']), "%Y-%m-%dT%H%M%S.%f"
            if delta_time.seconds() == 60:
                broken = False
            else:
                broken = True
            data.append({
                "tradingpair": trading_pair,
                "time": candle["time_period_start"],
                "open": float(candle["price_open"]),
                "close": float(candle["price_close"]),
                "low": float(candle["price_low"]),
                "high": float(candle["price_high"]),
                "volume": float(candle["volume_traded"]),
                "trades": float(candle["trades_count"]),
                "broken": broken
            })
        
        await SQLExecutor.async_insert(
            """
            INSERT INTO candle_data_1min (tradingpair, time, open, close, low, high, volume) VALUES
            """, data
        )
        date_end_while = date_end_while + timedelta(seconds=60000)
    # (количество минктных свеч из датасета / общее количество минутных свеч) * 100)

    broken_candles_quantity = await SQLExecutor.async_execute(f'''
    SELECT (({len(data)})/COUNT(*)) * 100) AS quantity
    FROM candle_data_1min
    ''')
    needed_symbol.quantity_broken_candles = broken_candles_quantity
    await needed_symbol.save()

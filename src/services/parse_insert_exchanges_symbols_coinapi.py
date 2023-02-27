import requests
import json
import os 
import datetime
from tortoise import Tortoise, exceptions
from models import Exchange, Symbols


exchanges_get = 'https://rest.coinapi.io/v1/exchanges'
tickets_get = 'https://rest.coinapi.io/v1/symbols'
OLD_API_KEY = 'AD143E2D-E5B8-4ECF-B292-06AA2E84AD3A'
NEW_API_KEY = 'C139C5E8-5C97-4A74-91AE-D6C08BF09E7D'





async def load_exchanges():

    exchanges = requests.get(
                    url=exchanges_get,
                    headers={
                        'X-CoinAPI-Key': OLD_API_KEY,
                        # 'content-type': "application/json"
                    }
                )
    if exchanges.status_code == 200:
        
        bulk_create_exchange = []
        for i in exchanges.json():
            bulk_create_exchange.append(
                Exchange(
                    exchange_id=i['exchange_id'],
                    website=i['website'],
                    name=i['name'],
                    data_symbols_count=i['data_symbols_count']
                )
            )
        try:
            await Exchange.bulk_create(bulk_create_exchange)
            print(len(bulk_create_exchange), "Количество бирж загружено")
        except exceptions.IntegrityError:
            print("Биржи уже залиты")


async def load_symbols():

    symbols = requests.get(
                url=tickets_get,
                headers={
                    'X-CoinAPI-Key': OLD_API_KEY,
                    # 'content-type': "application/json"
                }
            )
    if symbols.status_code == 200:

        bulk_create_symbols = []
        for i in symbols.json():
            if not i.get('asset_id_base', None):
                print("Кривая пара", i)
                continue
            bulk_create_symbols.append(
                Symbols(
                    symbol_id=i['symbol_id'],
                    exchange_id=i['exchange_id'],
                    symbol_type=i['symbol_type'],
                    asset_id_base=i['asset_id_base'],
                    asset_id_quote=i['asset_id_quote'],
                )
            )
        await Symbols.bulk_create(bulk_create_symbols)

        print(len(bulk_create_symbols), "Количество тикеров загружено")

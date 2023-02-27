import os
import re
import pyarrow.parquet as pq
from services.clickhouse_queries import insert_parquet_to_candle_data
from services.integrity_check import integrity_check


async def convert_time_of_ohlcv(interval):
    if interval == '1min':
        await write_1_min(interval)
        return

    for parquet in os.listdir('/app/data/'):
        file = re.split(r'[_/.]+', parquet)
        filename = file[0]
        if os.path.exists(f'/app/data/{filename}_{interval}.parquet'):
           return 0
        print("проверка существования файла вида {filename}_{interval}.parquet пройдена")

        table = pq.read_table(f'/app/data/{parquet}')

        panda = table.to_pandas()
        data = await integrity_check(panda)
        if data == 0:
            return 0
        print("проверка данных пройдена")
        period = None
        if re.search(r'h', interval):
            period = re.split(r'o', interval)[0]
        elif re.search(r'd', interval):
            period = re.split(r'a', interval)[0]
        elif re.search(r'm', interval):
            period = interval
        df = panda.resample(f'{period}')['open', 'high', 'low', 'close', 'volume', 'number_of_trades'].agg({
            "high": "max",
            "open": "first",
            "close": "last",
            "low": "min",
            "volume": "sum",
            "number_of_trades": "sum"
        }).interpolate()
        print("создан новый интервал")
        data = await integrity_check(df)
        if data == 0:
            return 0
        print("проверка данных пройдена")
        df.to_parquet(f"/app/data/{filename}_{interval}.parquet")
        print("передача данных на запись в бд")
        await write_to_clickhouse(interval)



async def write_1_min(interval):
    try:
        interval_list = []
        for parquet in os.listdir('/app/data/'):

            if not re.search(r'[_]', parquet):
                interval_list.append(parquet)
        print("добавлены монеты в лист для записи")
        for filename in interval_list:

            table = pq.read_table(f"/app/data/{filename}")
            pair = re.sub(f'[-/_{interval}/.parquet]+', '', filename)
            panda = table.to_pandas()
            data = await integrity_check(panda)
            if data == 0:
                return 0
            print("проверка данных пройдена")
            df = panda.reset_index()

            df_dict = df.to_dict('index')

            for values in df_dict.values():
                await insert_parquet_to_candle_data(pair=pair, dict=values, period=interval)
            print("запись в бд мутных завершена")
    except Exception as e:
        return e


async def write_to_clickhouse(interval):
    try:
        interval_list = []
        for parquet in os.listdir('/app/data/'):

            if re.search(rf'_{interval}', parquet):
                interval_list.append(parquet)
        print("добавлены монеты в лист для записи")
        for filename in interval_list:

            table = pq.read_table(f"/app/data/{filename}")
            pair = re.sub(f'[-/_{interval}/.parquet]+', '', filename)
            panda = table.to_pandas()
            df = panda.reset_index()

            df_dict = df.to_dict('index')

            for values in df_dict.values():
                await insert_parquet_to_candle_data(pair=pair, dict=values, period=interval)
            print("запись в бд мутных завершена")
            os.remove(f"/app/data/{filename}")
            print("удаление записанного файла")
    except Exception as e:
        return e

from services.converte_data import convert_time_of_ohlcv


async def fill_clickhouse_table():
    intervals = ["1min", "5min", "15min", "30min", "1hour", "4hours", "1day"]
    for interval in intervals:
        print(f"конвертирование {interval}")
        convert = await convert_time_of_ohlcv(interval)
        if convert == 0:
            return print(f"file exists with interval {interval}")

        print(interval)

    return print('ok')

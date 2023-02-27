



async def create_two_d_array(ohlcv: list):
    correct_ohlcv = []
    for i in ohlcv:
        correct_ohlcv.append(list(i.values()))
    return correct_ohlcv
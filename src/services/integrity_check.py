from fastapi import HTTPException

import pandas as pd
from starlette import status


async def integrity_check(dataframe: pd.DataFrame):


    count_nan = dataframe.isnull().sum().sum()
    if count_nan > 0 or dataframe.index.is_unique == False:
        return 0





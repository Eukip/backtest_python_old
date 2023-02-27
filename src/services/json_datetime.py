import json
import datetime
from json import JSONEncoder




class DateTimeEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


async def json_datetime(list):
    employeeJSONData = json.dumps(list,  cls=DateTimeEncoder)
    return employeeJSONData





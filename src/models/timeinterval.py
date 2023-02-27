import datetime

from fastapi_admin.models import AbstractAdmin
from tortoise import models, fields



class TimeInterval(models.Model):
    """
    The TimeFrame model
    """
    id = fields.BigIntField(pk=True)
    datetime_from = fields.DatetimeField()
    datetime_to = fields.DatetimeField()
    master_time = fields.ForeignKeyField("models.MasterTimeInterval", related_name='timeinterval', null=True)



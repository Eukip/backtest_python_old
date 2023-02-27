from enum import Enum

from tortoise import models, fields
import datetime


class OrderStatus(str, Enum):
    success = "выполнено успешно"
    fail = "не выполнено"
    pending = "в ожидании"


class Order(models.Model):
    """
    The Order model
    """
    id = fields.BigIntField(pk=True)
    open_price = fields.FloatField()
    open_time = fields.DatetimeField()
    amount = fields.FloatField()
    close_price = fields.FloatField(null=True)
    close_time = fields.DatetimeField(null=True)
    absolute_profit = fields.FloatField(null=True)
    profit_cer_period = fields.FloatField(null=True)
    profit_to_deposit = fields.FloatField(null=True)
    status = fields.CharEnumField(OrderStatus, null=True)
    predicted_time = fields.DatetimeField(null=True)
    # condition_in = fields.TextField(null=True)
    seconds_in_order = fields.IntField(null=True)
    deep = fields.FloatField(null=True)
    base = fields.TextField(null=True)
    base_price = fields.FloatField(null=True)
    pair = fields.ForeignKeyField('models.Pair', related_name='order')
    deal = fields.ForeignKeyField('models.Deal',
     related_name='order_deal', null=True)

    def __str__(self):
        return {self.amount}
        
    @property
    def time_in_order(self):
        value = None
        if self.close_time is None:
            value = datetime.datetime.now() - self.open_time
            # <class 'datetime.timedelta'> количество секунд
        else:
            value = self.close_time - self.open_time
            # <class 'datetime.timedelta'> количество секунд
        self.seconds_in_order = value.seconds
        self.save()
        return value

    class Meta:
        ordering = ["id"]

    class Config:
        orm_mode = True




from secrets import choice
from tortoise import models, fields


class Strategy(models.Model):
    """
    The Strategy model
    """
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=25, unique=True)
    base = fields.CharField(max_length=5, null=True)
    daily_turnover_from = fields.IntField(null=True)
    daily_turnover_to = fields.IntField(null=True)
    
    count_orders = fields.IntField(null=True)
    v_minus = fields.IntField(null=True)
    v_plus = fields.IntField(null=True)
    v_zero = fields.IntField(null=True)
    not_closed = fields.IntField(null=True)

    deal_depth_1 = fields.FloatField(null=True)
    deal_depth_2 = fields.FloatField(null=True)
    deal_depth_3 = fields.FloatField(null=True)
    
    profit_cer_period = fields.FloatField(null=True, default=22.22)
    profit_to_deposit = fields.FloatField(null=True, default=22.22)
    absolute_profit = fields.FloatField(null=True, default=0.02)
    
    png_from_xmind_input = fields.TextField(null=True)
    png_from_xmind_output = fields.TextField(null=True)
    moment_max_drawdown = fields.IntField(null=True, default=(-123))
    all_order_max_drawdown = fields.IntField(null=True, default=(-123))
    deposit_limit = fields.IntField(null=True, default=10)
    archived = fields.BooleanField(default=False)
    
    self_master: fields.ForeignKeyNullableRelation["models.Strategy"] = fields.ForeignKeyField("models.Strategy", related_name='self_master_strategy', null=True)
    deal_strategy: fields.ReverseRelation["models.Deal"]
    self_master_strategy = fields.ReverseRelation["models.Strategy"]


    def __str__(self):
        return f"{self.name}"


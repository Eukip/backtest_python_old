from tortoise import models, fields


class Deal(models.Model):
    """
    The Deal model
    """
    id = fields.BigIntField(pk=True)
    formula = fields.TextField()
    indicators = fields.JSONField()

    strategy = fields.ForeignKeyField('models.Strategy', related_name='deal_strategy')
    order_deal: fields.ReverseRelation["models.Order"]
    deal_formula: fields.ReverseRelation["models.Formula"]

    def __str__(self):
        return f"{self.id}"

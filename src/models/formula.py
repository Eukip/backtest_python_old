from tortoise import models, fields


class Formula(models.Model):
    """
    The Deal model
    """
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    formula = fields.TextField(null=True)
    deal = fields.ForeignKeyField('models.Deal', related_name='deal_formula', null=True)

    def __str__(self):
        return f"{self.name}"


from tortoise import models, fields



class Pair(models.Model):
    """
    The Pair model
    """
    id = fields.BigIntField(pk=True)
    trading_pair = fields.CharField(max_length=15)
    market = fields.CharField(max_length=25)

    order : fields.ReverseRelation["models.Order"]

    def __str__(self):
        return f"{self.trading_pair}"


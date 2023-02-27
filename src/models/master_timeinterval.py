from tortoise import models, fields



class MasterTimeInterval(models.Model):
    """
    The MasterTimeFrame model
    """
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=128)

    timeinterval: fields.ReverseRelation["models.TimeInterval"]


    def __str__(self):
        return f"{self.name}"

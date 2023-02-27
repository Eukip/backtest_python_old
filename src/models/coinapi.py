from tortoise import models, fields


class Exchange(models.Model):

    exchange_id = fields.CharField(pk=True, max_length=127)
    website = fields.CharField(max_length=55, null=True)
    name = fields.CharField(max_length=55, null=True)
    data_symbols_count = fields.IntField(null=True)

    symbol_exchange: fields.ReverseRelation['models.Symbols']


class Symbols(models.Model):
    
    symbol_id = fields.CharField(pk=True, max_length=127)
    exchange = fields.ForeignKeyField('models.Exchange', related_name="symbol_exchange")
    symbol_type = fields.CharField(max_length=55, null=True)
    asset_id_base = fields.CharField(max_length=55, null=True)
    asset_id_quote = fields.CharField(max_length=55, null=True)
    asset_id_unit = fields.CharField(max_length=55, null=True)
    data_start = fields.CharField(max_length=55, null=True)
    data_end = fields.CharField(max_length=55, null=True)
    data_quote_start = fields.CharField(max_length=100, null=True)
    data_quote_end = fields.CharField(max_length=100, null=True)
    quantity_broken_candles = fields.BigIntField(null=True)

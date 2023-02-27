from typing import Any

from fastapi_admin.app import app
from fastapi_admin.resources import Link, Model, Dropdown, Field, Action
from fastapi_admin.widgets import filters, inputs
from starlette.requests import Request

from models.user import User
from models.order import Order
from models.pair import Pair

@app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


class CustomModel(Model):

    @property
    def page_pre_title(self):
        return f'{self.label} list'

    @property
    def page_title(self):
        return self.label



class CostomForeignKey(inputs.ForeignKey):
    async def parse_value(self, request: Request, value: Any):
        is_nullable = self.context.get("null", False) is True
        if not value and is_nullable:
            return None
        model = self.model
        field_pk_attr = model._meta.pk_attr
        obj = await model.get(**{field_pk_attr: value})
        return obj


@app.register
class UserResource(CustomModel):
    label = 'User'
    model = User
    icon = 'fas fa-user'
    fields = [
        'id', 'login', 'email', 'created_at'
    ]

class OrderResource(CustomModel):
    label = 'Order'
    model = Order
    fields = [
        'id', 'direction', 'open_price', 'amount', 'close_price',
        Field('pair', input_=CostomForeignKey(Pair, default=None))
    ]
    filters = [
        filters.Filter(name='direction', label='direction'),
        filters.Filter(name='amount', label='amount'),
    ]


class PairResource(CustomModel):
    label = 'Pair'
    model = Pair
    fields = ['trading_pair', 'market',]
    filters = [
        filters.Filter(name='trading_pair', label='trading pair'),
    ]
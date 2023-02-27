import datetime

from fastapi_admin.models import AbstractAdmin
from tortoise import models, fields



class User(models.Model):
    """
    The User model
    """
    id = fields.BigIntField(pk=True)
    login = fields.CharField(max_length=128, null=True)
    email = fields.CharField(max_length=128, null=True)
    password = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]

    class Config:
        orm_mode = True





class Admin(AbstractAdmin):
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"
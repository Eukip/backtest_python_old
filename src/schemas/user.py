import re


import bleach
from pydantic import BaseModel, validator, EmailStr
from pydantic.schema import datetime




class UserBasePydantic(BaseModel):
    login: str
    password: str


class UserCreateRequest(UserBasePydantic):
    confirm_password: str


    @validator('login')
    def login_validate(cls, input_value):
        email_validator = EmailStr()
        email_validator.validate(input_value)

        if input_value != bleach.clean(input_value):
            raise ValueError('Invalid Login. Using HTML tags forbidden')

        return input_value


    @validator('password')
    def password_check_len(cls, input_value):
        if len(input_value) <= 6:
            raise ValueError('Password must be more than 6 chars')
        return input_value

    class Config:
        orm_mode = True

        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
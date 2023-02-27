from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from core.config import settings



def init_tortoise(app: FastAPI):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APPS_MODELS},
        generate_schemas=False,
        add_exception_handlers=True,
    )
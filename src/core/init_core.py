import os
from pathlib import Path
from fastapi_admin.app import app as admin_app
import aioredis
from fastapi import FastAPI
from fastapi_admin.providers.login import UsernamePasswordProvider
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from core.config import settings
# from core.content_size_middlewware import LimitUploadSize
from db import init_tortoise
from api.v1.api import api_router
from models.user import Admin
from fastapi_utils.tasks import repeat_every
from fastapi_pagination import add_pagination


def create_app():
    app = FastAPI(title='Altcoin Trader',
                  middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=['https://api.atbs.webinfra.ru'],
                allow_credentials=True,
                allow_methods=['*'],
                allow_headers=['*'],
            )
        ],)
    # app.add_middleware(LimitUploadSize, max_upload_size=50_000_000_000_000_000_000_000) # ~5000 mb
    Path("static/uploads").mkdir(parents=True, exist_ok=True)
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(settings.BASE_DIR, "static")),
        name="static",
    )


    @app.on_event("startup")
    async def startup():
        redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            decode_responses=True,
            encoding="utf8",
        )

        await admin_app.configure(
            logo_url='https://preview.tabler.io/static/logo_white.svg',
            template_folders=[os.path.join(settings.BASE_DIR, "src", "templates")],
            favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
            providers=[UsernamePasswordProvider(
                    admin_model=Admin,
                    login_logo_url="https://preview.tabler.io/static/logo.svg",
                )
                      ],
            redis=redis
        )

    app.mount("/admin", admin_app)

    init_tortoise(app)
    add_pagination(app)

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

import os
from typing import List

from fastapi import Depends
from fastapi_admin import app
from fastapi_admin.depends import get_resources
from fastapi_admin.template import templates
from starlette.requests import Request


@app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dashboard",
            "page_pre_title": "overview",
            "page_title": "Dashboard",
        },
    )
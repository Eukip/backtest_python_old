from fastapi.routing import APIRouter
from pydantic import BaseModel


class Status(BaseModel):
    status: str

router = APIRouter()


@router.get("/live", response_model=Status)
async def live():

    return Status(status="ok")
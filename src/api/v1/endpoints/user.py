from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from schemas.user import UserCreateRequest
from services import user_service
from models.user import User
from services.auth import auth_handler



router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str


class AuthDetails(BaseModel):
    login: str
    password: str



@router.post(
    "/create_user",
    response_model=Token
)
async def create_user(user_details: UserCreateRequest):

    email = None


    if await user_service.is_email(email=user_details.login):
        if await user_service.is_exist_by_email(email=user_details.login) is True:
            raise HTTPException(status_code=400, detail='Login is taken')
        else:
            email = user_details.login.lower()

    user_orm = User(
        login=email,
        email=email,
        password=auth_handler.get_password_hash(user_details.password),
    )
    await user_orm.save()


    access_token = auth_handler.encode_token(user_orm.id)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/auth", response_model=Token)
async def auth(auth_details: AuthDetails):
    user_orm = None

    if await user_service.is_email(email=auth_details.login):
        user_orm = await User.get_or_none(email=auth_details.login.lower())

    if not user_orm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User login not found',
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not auth_handler.verify_password(auth_details.password, user_orm.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_handler.encode_token(user_orm.id)
    return Token(access_token=access_token, token_type="bearer")

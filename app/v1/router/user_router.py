from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.v1.schema import user_schema
from app.v1.service import user_service
from app.v1.service import auth_service
from app.v1.schema.token_schema import Token


router = APIRouter(prefix="/api/v1")


@router.post(
    "/user",
    response_model=user_schema.UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user: user_schema.UserIn):
    return user_service.create_user(user)


@router.post(
    "/login",
    tags=["users"],
    response_model=Token
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = auth_service.generate_token(
        form_data.username, form_data.password)
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/user/{user_id}",
    response_model=user_schema.UserOut
)
async def get_user_by_id(user_id: int):
    return user_service.get_user_by_id(user_id)


@router.patch("/user/change_password")
async def change_password(
        change_password: user_schema.ChangePassword,
        current_user: user_schema.UserOut = Depends(auth_service.get_current_user)):
    return user_service.change_password(change_password, current_user)

from fastapi import APIRouter
from fastapi import status

from app.v1.schema import user_schema
from app.v1.service import user_service

router = APIRouter(prefix="/api/v1")

@router.post(
    "/user",
    response_model=user_schema.UserOut,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: user_schema.UserIn):
    return user_service.create_user(user)






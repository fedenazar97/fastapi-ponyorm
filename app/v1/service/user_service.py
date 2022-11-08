from fastapi import HTTPException, status

from app.v1.model.user_model import User as UserModel
from app.v1.schema import user_schema
from app.v1.service.auth_service import passwrd_hashed, verify_password, get_user

from pony.orm import db_session


def create_user(user_request: user_schema.UserIn):
    with db_session:
        get_user = UserModel.select(lambda u: u.username == user_request.username
                                    or u.mail == user_request.mail
                                    ).first()
        if get_user:
            msg = "Email already registered"
            if get_user.username == user_request.username:
                msg = "Username already registered"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=msg
            )
        user = UserModel(
            username=user_request.username,
            password=passwrd_hashed(user_request.password),
            mail=user_request.mail)
    return user_schema.UserOut(
        id=user.id,
        username=user.username,
        operation_result='Succesfully created !'
    )


def get_user_by_id(user_id: int):
    with db_session:
        user = UserModel.get(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
    return user_schema.UserOut(
        id=user.id,
        username=user.username,
        operation_result='user found'
    )


@db_session
def change_password(change_password_obj: user_schema.ChangePassword, user: user_schema.UserOut):
    res_user = get_user(user.username)
    valid = verify_password(
        change_password_obj.current_password, res_user.password)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password incorrect"
        )
    if change_password_obj.new_password != change_password_obj.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="New password is not match"
        )
    res_user.password = passwrd_hashed(change_password_obj.new_password)
    return user_schema.UserOut(
        id=res_user.id,
        username=res_user.username,
        operation_result='The password has been changed successfully'
    )

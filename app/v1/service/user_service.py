from fastapi import HTTPException, status

from app.v1.model.user_model import User as UserModel
from app.v1.schema import user_schema

from pony.orm import db_session

import bcrypt

def passwrd_hashed(passwrd: str):
    bytes = passwrd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

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
        user= UserModel (
            username= user_request.username,
            password= str(passwrd_hashed(user_request.password)),
            mail= user_request.mail)
    return user_schema.UserOut(
        id= user.id, 
        username= user.username,
        operation_result= 'Succesfully created !'
    )
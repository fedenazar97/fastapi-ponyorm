from pydantic import BaseModel, EmailStr
from typing import Optional

class UserIn(BaseModel):
    username: str
    password: str
    mail: EmailStr

class UserOut(BaseModel):
    id: int
    username: str
    operation_result: Optional[str] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str   
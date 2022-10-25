from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    mail: EmailStr

class UserOut(BaseModel):
    id: int
    username: str
    operation_result: str    
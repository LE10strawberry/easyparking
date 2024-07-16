from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    surname: str
    phone: str
    email: EmailStr
    password: str
    user_type: str

class User(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    email: EmailStr
    user_type: str

# 这个设置告诉 Pydantic 在数据模型转换时，要以 ORM 模式处理数据。1. 自动转换数据库模型 2.处理数据库特有的返回数据
    class Config:
        orm_mode = True
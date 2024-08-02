from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional as optional

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


class User(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    email: EmailStr
    user_type: str
    created_at: datetime

# 这个设置告诉 Pydantic 在数据模型转换时，要以 ORM 模式处理数据。1. 自动转换数据库模型 2.处理数据库特有的返回数据
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSearch(BaseModel):
    id: int
    name: str
    surname: str
    phone: str
    email: EmailStr
    user_type: str
    # created_at: datetime
    created_at: str

    # from_user 是一个类方法 (@classmethod)，用于从一个 User 对象创建一个 UserSearch 对象。
    @classmethod
    def from_user(cls, user: User):
        return cls(
            id=user.id,
            name=user.name,
            surname=user.surname,
            phone=user.phone,
            email=user.email,
            user_type=user.user_type,
            # created_at=user.created_at,
            # created_at=user.created_at.date()
            created_at=user.created_at.strftime("%Y-%m-%d")  # 格式化为 yyyy-MM-dd 字符串
        )

class ParkingRecordCreat(BaseModel):
    user_id: int
    user_name: str
    parking_location_id: int
    parking_location_name: str
    cost_per_hour: float
    check_in_type: str
    check_in_time: optional[datetime]  = None
    order_status: optional[str]  = None
    created_at: optional[datetime] = None
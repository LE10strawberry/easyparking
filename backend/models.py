from sqlalchemy import Column, Integer, String, DateTime, func
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50),nullable=False, comment='姓名')
    surname = Column(String(50),nullable=False, comment='姓')
    phone = Column(String(20), unique=True, comment='电话')
    email = Column(String(100), unique=True, comment='邮箱')
    password = Column(String(100), comment='密码')
    user_type = Column(String(50), comment='用户类型, admin, normal')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')


    __table_args__ = {'extend_existing': True}

    # __mapper_args__ = {"order_by": id}
    #
    # def __repr__(self):
    #     return f"<User {self.name}, {self.email}>"
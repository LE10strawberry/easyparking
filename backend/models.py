from sqlalchemy import Column, Integer, String, DateTime, func, DECIMAL
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


class ParkingLocation(Base):
    __tablename__ = 'parking_location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(60), nullable=True, comment='Parking location')
    description = Column(String(255), nullable=True, comment='Parking location description')
    capacity = Column(Integer, nullable=True, comment='Parking capacity')
    available = Column(Integer, nullable=True, comment='available capacity')
    status = Column(String(60), nullable=True, comment='Parking available status: full, available')
    cost_per_hour = Column(DECIMAL(10, 2), nullable=True, comment='Cost per hour')
    created_at = Column(DateTime, server_default=func.now(), comment='creation time')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='update time')

class ParkingRecord(Base):
    __tablename__ = 'parking_record'
    __table_args__ = {'comment': 'Parking Recording'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, comment='User ID')
    username = Column(String(100), nullable=True, comment='User name')
    parking_location_id = Column(Integer, nullable=True, comment='Parking location ID')
    parking_location = Column(String(60), nullable=True, comment='Parking location')
    check_in_time = Column(DateTime, nullable=True, comment='Check-in time')
    packing_hours = Column(Integer, nullable=True, comment='Parking hours')
    check_out_time = Column(DateTime, nullable=True, comment='Check-out time')
    cost_per_hour = Column(DECIMAL(10, 2), nullable=True, comment='Cost per hour')
    total_cost = Column(DECIMAL(10, 2), nullable=True, comment='Total cost')
    order_status = Column(String(60), nullable=True, comment='Order status: active, completed')
    created_at = Column(DateTime, server_default=func.now(), comment='creation time')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='update time')

    # 使用现有的表并在其基础上进行扩展（添加新的列或约束等），而不是尝试创建一个全新的表结构
    __table_args__ = {'extend_existing': True}

    # __mapper_args__ = {"order_by": id}
    # def __repr__(self):
    # return f"<User {self.name}, {self.email}>"

def __repr__(self):
    return f"<ParkingLocation(id={self.id}, location='{self.location}', capacity={self.capacity})>"
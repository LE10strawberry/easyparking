from sqlalchemy.orm import Session
from backend import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# check user exist or not by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    # check password is name with check_password_hash
    # if user.password != user.check_password:
    #     return False

    hashed_password= pwd_context.hash(user.password)

    db_user = models.User(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        password=hashed_password,
        user_type=user.user_type
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def search_users(db: Session, id: int = None, name: str = None, surname: str = None, phone: str = None, email: str = None, user_type: str = None):
    query = db.query(models.User)
    if id:
        query = query.filter(models.User.id == id)
    if name:
        # LIKE 用于根据指定的模式进行搜索。可以使用通配符，例如 %（匹配零个或多个字符）和 _（匹配一个字符）
        query = query.filter(models.User.name.like(f"%{name}%"))
    if surname:
        query = query.filter(models.User.surname.like(f"%{surname}%"))
    if phone:
        query = query.filter(models.User.phone.like(f"%{phone}%"))
    if email:
        query = query.filter(models.User.email.like(f"%{email}%"))
    if user_type != "all":
        query = query.filter(models.User.user_type == user_type)
    return query.all()

# location search by multi conditions：Location Name，Description，Available Status，should be able to Fuzzy matching query
def get_locations(db: Session, location_name: str = None, description: str = None, available_status: str = None):
    query = db.query(models.ParkingLocation)
    if location_name:
        query = query.filter(models.ParkingLocation.location.like(f"%{location_name}%"))
    if description:
        query = query.filter(models.ParkingLocation.description.like(f"%{description}%"))
    if available_status != "all":
        query = query.filter(models.ParkingLocation.status == available_status)
    return query.all()

# query actived parking record by multi conditions, support fuzzy query, support query by ID，User Name，Parking Location
def checked_in(parkingRecordCreat:schemas.ParkingRecordCreat, db: Session):
    # 判断是自己check-in还是admin check-in
        # 如果是自己check-in
            # 从前端传递用户信息
        # 如果是admin check-in
            # 从session中获取用户信息
    # 获取停车场每小时价格
    # 保存到check-in表中
    # 更新停车场available数

    # check if it is available of parking lot according to the parking location id
    parking_location = db.query(models.ParkingLocation).filter(models.ParkingLocation.id == parkingRecordCreat.parking_location_id).first()

    # check parking_location is not null
    if parking_location is None:
        return "Parking location not found"
    if parking_location.available == 0:
        return "Parking lot is full"

    # save parking record to database
    db_parking_record = models.ParkingRecord(
        user_id=parkingRecordCreat.user_id,
        username=parkingRecordCreat.user_name,
        parking_location_id=parkingRecordCreat.parking_location_id,
        parking_location=parkingRecordCreat.parking_location_name,
        check_in_time= datetime.now(),
        cost_per_hour=parkingRecordCreat.cost_per_hour,
        order_status="active"
    )
    db.add(db_parking_record)

    # update parking location available
    parking_location.available -= 1
    if parking_location.available == 0:
        parking_location.status = "full"
        return "Parking lot is full"

    db.add(parking_location)
    db.commit()
    db.refresh(db_parking_record)

    return "Check-in successfully"

def search_checked_in(db: Session, id: int = None, username: str = None, location: str = None):
    query = db.query(models.ParkingRecord)
    if id:
        query = query.filter(models.ParkingRecord.id == id)
    if username:
        query = query.filter(models.ParkingRecord.username.like(f"%{username}%"))
    if location:
        query = query.filter(models.ParkingRecord.parking_location.like(f"%{location}%"))
    # only return active parking records
    query = query.filter(models.ParkingRecord.order_status == "active")
    return query.all()
from sqlalchemy.orm import Session
from backend import models, schemas
from passlib.context import CryptContext
# pip install fastapi uvicorn sqlalchemy pymysql alembic passlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
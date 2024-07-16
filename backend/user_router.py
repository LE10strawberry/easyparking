from fastapi import APIRouter, FastAPI, Depends, HTTPException
from backend import crud, models, schemas,database
from backend.database import SessionLocal, engine
from sqlalchemy.orm import Session

router_main = APIRouter()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create new user
@router_main.post("/create_user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router_main.get("/")
async def root():
    return {"message": "Hello World"}
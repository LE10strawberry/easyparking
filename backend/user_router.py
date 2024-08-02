from fastapi import APIRouter, Depends, HTTPException, Response, status, Form, Query
from backend import models, schemas, crud
from backend.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from typing import Optional

# from fastapi import Request 请求相关模板页面
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='./project/templates')
from urllib.parse import unquote,quote

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

# login for user, parameter: email, password
@router_main.post("/login")
async def login_user(request: Request, response: Response, user: schemas.UserLogin, db: Session = Depends(get_db)):
    # check if email exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        return JSONResponse(content=jsonable_encoder("Email not found"), status_code=status.HTTP_400_BAD_REQUEST)
        # raise HTTPException(status_code=404, detail="Email not found")
    # check if password is correct
    if not crud.verify_password(user.password, db_user.password):
        return JSONResponse(content=jsonable_encoder("Password incorrect"), status_code=status.HTTP_400_BAD_REQUEST)
        # raise HTTPException(status_code=400, detail="Password incorrect")

    # return user info by json
    return JSONResponse(content=jsonable_encoder(db_user), status_code=status.HTTP_200_OK)

 # search user by multi conditions, parameter: id, name, surname, phone, email, user_type
@router_main.post("/search_users")
async def search_users(id: Optional[int] = Form(None),
                       name: Optional[str] = Form(None),
                       surname: Optional[str] = Form(None),
                       phone: Optional[str] = Form(None),
                       email: Optional[str] = Form(None),
                       user_type: Optional[str] = Form(None),
                       db: Session = Depends(get_db)):
    # 在这里处理收到的用户名和密码
    user = crud.search_users(db, id=id, name=name, surname=surname, phone=phone, email=email, user_type=user_type)
    # 可以在这里添加处理逻辑，比如验证用户信息，存储到数据库等
    return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_200_OK)


# search actived parking record by multi conditions, parameter: id, username,parking_location
@router_main.post("/search_checked_in")
async def search_checked_in(id: Optional[int] = Form(None), username: Optional[str] =  Form(None), location:Optional[str] = Form(None), db: Session = Depends(get_db)):
    user = crud.search_checked_in(db, id=id, username=username, location=location)
    return JSONResponse(content=jsonable_encoder(user), status_code=status.HTTP_200_OK)


@router_main.get("/hello1/{name}")
async def say_hello(name: str, q: Optional[str] = None):
    return {"message": f"Hello {name}", "q":q}


@router_main.get("/search_locations")
async def search_locations(location_name: Optional[str] = None, description: Optional[str] = None, available_status: Optional[str] = None, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, location_name=location_name, description=description, available_status=available_status)
    return JSONResponse(content=jsonable_encoder(locations), status_code=status.HTTP_200_OK)


@router_main.get("/login_page", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})


@router_main.get("/register_page", response_class=HTMLResponse)
async def another_page(request: Request):
    return templates.TemplateResponse("Register.html", {"request": request})


@router_main.get("/location_page", response_class=HTMLResponse)
async def another_page(request: Request):
    return templates.TemplateResponse("Location.html", {"request": request})


@router_main.get("/location_edit_page", response_class=HTMLResponse)
async def another_page(request: Request,
                       id: int,
                       location: str,
                       cost_per_hour: int,
                       capacity: int,
                       description: str
                       ):

    location = unquote(location)
    description = unquote(description)
    return templates.TemplateResponse("Location_edit.html", {
        "request": request,
        "id": id,
        "location": location ,
        "cost_per_hour": cost_per_hour,
        "capacity": capacity,
        "description": description})


@router_main.get("/parking_page", response_class=HTMLResponse)
async def another_page(request: Request):
    return templates.TemplateResponse("Parking.html", {"request": request})

@router_main.get("/user_page", response_class=HTMLResponse)
async def another_page(request: Request):
    return templates.TemplateResponse("User.html", {"request": request})


@router_main.get("/checked_in", response_class=HTMLResponse)
# async def checked_in(parkingRecord: schemas.ParkingRecordCreat, db: Session = Depends(get_db)):
async def checked_in(
    request: Request,
    user_id: int = Query(...),
    user_name: str = Query(...),
    parking_location_id: int = Query(...),
    parking_location_name: str = Query(...),
    cost_per_hour: float = Query(..., alias="cost_per_hour"),
    check_in_type: str = Query(..., alias="check_in_type"),
    db: Session = Depends(get_db)
    ):
    # 创建 ParkingRecordCreate 对象，并自动验证数据
    parking_record = schemas.ParkingRecordCreat(
        user_id=user_id,
        user_name=user_name,
        parking_location_id=parking_location_id,
        parking_location_name=parking_location_name,
        cost_per_hour=cost_per_hour,
        check_in_type=check_in_type
    )
    message = crud.checked_in(parking_record, db)
    return templates.TemplateResponse("Location.html", {"request": request, "message": message})
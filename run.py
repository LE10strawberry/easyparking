import uvicorn
from fastapi import FastAPI
from backend import router_main
from fastapi.staticfiles import StaticFiles


# from tutorial import app03, app04, app05, app06, app07, app08

# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title='Easy Parking API Docs',
    description='Easy Parking API接口文档。系统→用于停车场管理。',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
app.mount(path='/static', app=StaticFiles(directory='./backend/static'), name='static')  # .mount()不要在分路由APIRouter().mount()调用，模板会报错

# @app.middleware('http')
# async def add_process_time_header(request: Request, call_next): # call_next将接受request请求...(截图没了)
# start_time = time.time()
# response = await call_next(request)
# process_time = time.time() - start_time
# response.headers['X-Process-Time'] = str(process_time) #添加自定义的以“X-”开头的请求头


# app.include_router(location, prefix='/location', tags=['停车场位置信息模块API'])
# app.include_router(parking, prefix='/parking', tags=['停车场订单模块API'])
app.include_router(router_main, prefix='/easyparking', tags=['Easy Parking API'])

if __name__ == '__main__':
    uvicorn.run('run:app', host='127.0.0.1', port=8000, reload=True, workers=3)

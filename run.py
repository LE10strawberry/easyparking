#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Yan__'

import uvicorn
from fastapi import FastAPI

from backend import router_main

# from tutorial import app03, app04, app05, app06, app07, app08

app = FastAPI(
    title='Easy Parking API Docs',
    description='Easy Parking API接口文档。',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

# app.include_router(location, prefix='/location', tags=['停车场位置信息模块API'])
# app.include_router(parking, prefix='/parking', tags=['停车场订单模块API'])
app.include_router(router_main, prefix='/easyparking', tags=['Easy Parking API'])

if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, workers=3)
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

from settings import TORTOISE_ORM
from router import office, gymrrom, subscriprion

app = FastAPI(description='API FOR CRM')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    add_exception_handlers=False
)

app.include_router(office.router)
app.include_router(gymrrom.router)
app.include_router(subscriprion.router)
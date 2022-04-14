import uuid
from typing import List

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

import models
from schema import Office_Pydantic, GymRoom_Pydantic, GymRoom_OfficePK_Pydantic, Office_Raw_Pydantic
from models import Office, GymRoom
from settings import TORTOISE_ORM

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


@app.get('/office', response_model=List[Office_Pydantic])
async def office_all():
    get_all_office = Office.all()
    return await Office_Pydantic.from_queryset(get_all_office)


@app.post('/office', response_model=Office_Raw_Pydantic)
async def add_office(office: Office_Raw_Pydantic):
    new_office = office.dict()
    new_office['uid'] = uuid.uuid4()
    create_doc = await models.Office.create(**new_office)
    return await Office_Raw_Pydantic.from_tortoise_orm(create_doc)


@app.put('/office/{uid:uuid}', response_model=Office_Raw_Pydantic)
async def update_office(uid: uuid.UUID, office: Office_Raw_Pydantic):
    get_office = await models.Office.get(uid=uid)
    get_office = await get_office.update_from_dict(office.dict())
    await get_office.save()
    return await Office_Raw_Pydantic.from_tortoise_orm(get_office)


@app.get('/office/{uid:uuid}', response_model=Office_Pydantic)
async def get_one_office(uid: uuid.UUID):
    get_office = await models.Office.get(uid=uid)
    return await Office_Pydantic.from_tortoise_orm(get_office)


@app.get('/gymroom', response_model=List[GymRoom_Pydantic])
async def gymroom_all():
    get_gym_all = GymRoom.all()
    return await GymRoom_Pydantic.from_queryset(get_gym_all)


@app.post('/gymroom', response_model=GymRoom_OfficePK_Pydantic)
async def gymroom_create(gymroom: GymRoom_OfficePK_Pydantic):
    get_office = models.Office.get(uid=gymroom.office)
    gymroom.office = get_office
    create_gymroom = await models.GymRoom.create(**gymroom.dict())
    return await GymRoom_OfficePK_Pydantic.from_tortoise_orm(create_gymroom)


@app.get('/gymroom/{uid:uuid}', response_model=GymRoom_Pydantic)
async def get_one_gymroom(uid: uuid.UUID):
    get_gym = await GymRoom.get(uid=uid)
    return await GymRoom_Pydantic.from_queryset(get_gym)

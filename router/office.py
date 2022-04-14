import uuid
from typing import List

from fastapi import APIRouter

import models
from schema import Office_Pydantic, Office_Raw_Pydantic
from models import Office


router = APIRouter(
    tags=['API Office']
)


@router.get('/office', response_model=List[Office_Pydantic])
async def office_all():
    get_all_office = Office.all()
    return await Office_Pydantic.from_queryset(get_all_office)


@router.post('/office', response_model=Office_Raw_Pydantic)
async def add_office(office: Office_Raw_Pydantic):
    new_office = office.dict()
    new_office['uid'] = uuid.uuid4()
    create_doc = await models.Office.create(**new_office)
    return await Office_Raw_Pydantic.from_tortoise_orm(create_doc)


@router.put('/office/{uid:uuid}', response_model=Office_Raw_Pydantic)
async def update_office(uid: uuid.UUID, office: Office_Raw_Pydantic):
    get_office = await models.Office.get(uid=uid)
    get_office = await get_office.update_from_dict(office.dict())
    await get_office.save()
    return await Office_Raw_Pydantic.from_tortoise_orm(get_office)


@router.get('/office/{uid:uuid}', response_model=Office_Pydantic)
async def get_one_office(uid: uuid.UUID):
    get_office = await models.Office.get(uid=uid)
    return await Office_Pydantic.from_tortoise_orm(get_office)


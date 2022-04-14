import uuid
from typing import List

from fastapi import APIRouter

import models
from schema import GymRoom_Pydantic, GymRoom_OfficePK_Pydantic
from models import GymRoom

router = APIRouter(
    tags=['API Gymroom']
)


@router.get('/gymroom', response_model=List[GymRoom_Pydantic])
async def gymroom_all():
    get_gym_all = GymRoom.all()
    return await GymRoom_Pydantic.from_queryset(get_gym_all)


@router.post('/gymroom', response_model=GymRoom_OfficePK_Pydantic)
async def gymroom_create(gymroom: GymRoom_OfficePK_Pydantic):
    get_office = models.Office.get(uid=gymroom.office)
    gymroom.office = get_office
    create_gymroom = await models.GymRoom.create(**gymroom.dict())
    return await GymRoom_OfficePK_Pydantic.from_tortoise_orm(create_gymroom)


@router.get('/gymroom/{uid:uuid}', response_model=GymRoom_Pydantic)
async def get_one_gymroom(uid: uuid.UUID):
    get_gym = await GymRoom.get(uid=uid)
    return await GymRoom_Pydantic.from_queryset(get_gym)
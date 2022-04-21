import uuid
from typing import List

from fastapi import APIRouter

import models
from schema import GymRoom_Raw_Pydantic, GymRoom_Pydantic
from models import GymRoom

router = APIRouter(
    tags=['API Gymroom']
)


@router.get('/gymroom', response_model=List[GymRoom_Pydantic])
async def gymroom_all():
    get_gym_all = GymRoom.all()
    return await GymRoom_Pydantic.from_queryset(get_gym_all)


@router.get('/gymroom/{uid:uuid}', response_model=GymRoom_Pydantic)
async def get_one_gymroom(uid: uuid.UUID):
    get_gym = await GymRoom.get(uid=uid)
    return await GymRoom_Pydantic.from_queryset(get_gym)


@router.put('/gymroom/{uid:uuid}', response_model=GymRoom_Raw_Pydantic)
async def update_gymroom(uid: uuid.UUID, gymroom: GymRoom_Raw_Pydantic):
    get_gym = await models.GymRoom.get(uid=uid)
    update_gym = await get_gym.update_from_dict(gymroom.dict())
    await update_gym.save()
    return await GymRoom_Raw_Pydantic.from_tortoise_orm(update_gym)


@router.delete('/gymroom/{uid:uuid}', response_model=GymRoom_Raw_Pydantic)
async def delete_gym(uid: uuid.UUID):
    get_gym = await models.GymRoom.get(uid=uid)
    await get_gym.delete()
    return {'msg': "GymRoom delete successful"}


@router.post('/gymroom', response_model=GymRoom_Raw_Pydantic)
async def gymroom_create(gymroom: GymRoom_Raw_Pydantic):
    get_office = models.Office.get(uid=gymroom.office)
    gymroom.office = get_office
    create_gymroom = await models.GymRoom.create(**gymroom.dict())
    return await GymRoom_Raw_Pydantic.from_tortoise_orm(create_gymroom)

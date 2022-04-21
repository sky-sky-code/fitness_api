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


@router.put('/gymroom/{uid:uuid}', response_model=GymRoom_Pydantic)
async def update_gymroom(uid: uuid.UUID, gymroom: GymRoom_Raw_Pydantic):
    get_gym = await models.GymRoom.get(uid=uid)
    update_gym = await get_gym.update_from_dict(gymroom.dict())
    await update_gym.save()
    return await GymRoom_Pydantic.from_tortoise_orm(update_gym)


@router.delete('/gymroom/{uid:uuid}')
async def delete_gym(uid: uuid.UUID):
    get_gym = await models.GymRoom.get(uid=uid)
    await get_gym.delete()
    return {'msg': f"GymRoom {get_gym.name} delete successful"}


@router.post('/gymroom', response_model=GymRoom_Pydantic)
async def gymroom_create(gymroom: GymRoom_Raw_Pydantic):
    get_office = await models.Office.get(uid=gymroom.office_id)
    gymroom.office_id = get_office.uid
    create_gymroom = await models.GymRoom.create(**gymroom.dict())
    return await GymRoom_Pydantic.from_tortoise_orm(create_gymroom)

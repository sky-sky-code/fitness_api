import uuid
from typing import List, Optional

from fastapi import APIRouter

import models
from filter import filter_qs
from schema import GymRoom_Raw_Pydantic, GymRoom_Pydantic, GymLesson_Pydantic, GymLesson_Raw_Pydantic
from models import GymRoom, GymLesson

router = APIRouter(
    tags=['API Gymroom']
)


@router.get('/gymroom', response_model=List[GymRoom_Pydantic])
async def gymroom_all(name: Optional[str] = None, office: Optional[uuid.UUID] = None):
    data_gymroom = await filter_qs(models.GymRoom, GymRoom_Pydantic, name=name, office_id=office)
    return data_gymroom


@router.get('/gymroom/{uid:uuid}', response_model=GymRoom_Pydantic)
async def get_one_gymroom(uid: uuid.UUID):
    get_gym = await GymRoom.get(uid=uid)
    return await GymRoom_Pydantic.from_tortoise_orm(get_gym)


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


@router.get('/gymlesson', response_model=List[GymLesson_Pydantic])
async def get_all_gymlesson(name: Optional[str] = None, duration: Optional[str] = None, type: Optional[str] = None):
    data_gymlesson = await filter_qs(models.GymLesson, GymLesson_Pydantic, name=name, duration=duration, type=type)
    return data_gymlesson


@router.get('/gymlesson/{uid:uuid}', response_model=GymLesson_Pydantic)
async def get_gymlesson(uid: uuid.UUID):
    gymleson = await models.GymLesson.get(uid=uid)
    return await GymLesson_Pydantic.from_tortoise_orm(gymleson)


@router.put('/gymlesson/{uid:uuid}', response_model=GymLesson_Pydantic)
async def update_gymlesson(uid: uuid.UUID, gymlesson: GymLesson_Raw_Pydantic):
    gymlesson_get = await models.GymLesson.get(uid=uid)
    gymlesson = await gymlesson_get.update_from_dict(gymlesson.dict())
    await gymlesson.save()
    return await GymLesson_Pydantic.from_tortoise_orm(gymlesson)


@router.delete('/gymlesson/{uid:uuid}')
async def delete_gymlesson(uid: uuid.UUID):
    gymlesson = await models.GymLesson.get(uid=uid)
    await gymlesson.delete()
    return {'msg': f'GymLesson {gymlesson.name} delete successful'}


@router.post('/gymlesson', response_model=GymLesson_Pydantic)
async def create_gymlesson(gymlesson: GymLesson_Raw_Pydantic):
    gymlesson = gymlesson.dict()
    gymlesson['uid'] = uuid.uuid4()
    gymlesson = await models.GymLesson.create(**gymlesson)
    return await GymLesson_Pydantic.from_tortoise_orm(gymlesson)

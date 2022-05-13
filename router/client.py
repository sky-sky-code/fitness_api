import uuid
from typing import List

from fastapi import APIRouter
import models
from schema import Profile_Pydantic, Profile_Raw_Pydantic

router = APIRouter(
    tags=['API Client']
)


@router.get('/client', response_model=List[Profile_Pydantic])
async def get_client():
    clients = models.Profile.all()
    return await Profile_Pydantic.from_queryset(clients)


@router.post('/client', response_model=Profile_Pydantic)
async def create_client(data_client: Profile_Raw_Pydantic):
    data_client = data_client.dict()
    data_client['uid'] = uuid.uuid4()
    client = await models.Profile.create(**data_client)
    return await Profile_Pydantic.from_tortoise_orm(client)


@router.get('/client/{uid:uuid}', response_model=Profile_Pydantic)
async def get_one_client(uid: uuid.UUID):
    client = await models.Profile.get(uid=uid)
    return await Profile_Pydantic.from_tortoise_orm(client)


@router.put("/client/{uid:uuid}", response_model=Profile_Pydantic)
async def update_client(uid: uuid.UUID, data_client: Profile_Raw_Pydantic):
    user = await models.Profile.get(uid=uid)
    client = await user.update_from_dict(data_client.dict())
    await client.save()
    return await Profile_Pydantic.from_tortoise_orm(client)


@router.delete("/client/{uid:uuid}")
async def delete_client(uid: uuid.UUID):
    get_client = await models.Profile.get(uid=uid)
    await get_client.delete()
    return {'msg': f'Delete {get_client.name} {get_client.pat_name} {get_client.surname} client successful'}

import uuid
from typing import List

from fastapi import APIRouter
import models
from schema import Client_Pydantic, Client_Raw_Pydantic

router = APIRouter(
    tags=['API Client']
)


@router.get('/client', response_model=List[Client_Pydantic])
async def get_client():
    clients = models.User.all()
    return await Client_Pydantic.from_queryset(clients)


@router.post('/client', response_model=Client_Pydantic)
async def create_client(data_client: Client_Raw_Pydantic):
    data_client = data_client.dict()
    data_client['uid'] = uuid.uuid4()
    client = await models.User.create(**data_client)
    return await Client_Pydantic.from_tortoise_orm(client)


@router.get('/client/{uid:uuid}', response_model=Client_Pydantic)
async def get_one_client(uid: uuid.UUID):
    client = await models.User.get(uid=uid)
    return await Client_Pydantic.from_tortoise_orm(client)


@router.put("/client/{uid:uuid}", response_model=Client_Pydantic)
async def update_client(uid: uuid.UUID, data_client: Client_Raw_Pydantic):
    user = await models.User.get(uid=uid)
    client = await user.update_from_dict(data_client.dict())
    await client.save()
    return await Client_Pydantic.from_tortoise_orm(client)


@router.delete("/client/{uid:uuid}")
async def delete_client(uid: uuid.UUID):
    get_client = await models.User.get(uid=uid)
    await get_client.delete()
    return {'msg': f'Delete {get_client.name} {get_client.pat_name} {get_client.surname} client successful'}

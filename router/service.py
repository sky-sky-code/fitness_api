import uuid
from typing import List

from fastapi import APIRouter
from schema import Service_Pydantic, Service_Raw_Pydantic
import models

router = APIRouter(
    tags=['API Service']
)


@router.get('/service', response_model=List[Service_Pydantic])
async def get_service():
    get_qs = models.Service.all()
    return await Service_Pydantic.from_queryset(get_qs)


@router.post('/service', response_model=Service_Pydantic)
async def create_service(service: Service_Raw_Pydantic):
    service_dct = service.dict()
    service_dct['uid'] = uuid.uuid4()
    get_obj = await models.Service.create(**service_dct)
    return await Service_Pydantic.from_tortoise_orm(get_obj)


@router.get('/service/{uid:uuid}', response_model=Service_Pydantic)
async def get_one_service(uid: uuid.UUID):
    get_obj = await models.Service.get(uid=uid)
    return await Service_Pydantic.from_tortoise_orm(get_obj)


@router.put('/service/{uid:uuid}', response_model=Service_Pydantic)
async def update_service(uid: uuid.UUID, service: Service_Raw_Pydantic):
    get_obj = await models.Service.get(uid=uid)
    update_obj = await get_obj.update_from_dict(service.dict())
    await update_obj.save()
    return await Service_Pydantic.from_tortoise_orm(update_obj)


@router.delete('/service/{uid:uuid}')
async def delete_service(uid: uuid.UUID):
    get_obj = await models.Service.get(uid=uid)
    await get_obj.delete()
    return {'msg': f"Услуга '{get_obj.name}' удалена"}

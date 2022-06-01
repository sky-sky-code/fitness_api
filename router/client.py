import uuid
from typing import List
from datetime import datetime, timedelta

from fastapi import APIRouter
import models
from schema import Profile_Pydantic, Profile_Raw_Pydantic, \
    PurchasedSubscription_Pydantic, PurchasedSubscription_Raw_Pydantic

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


@router.get('/client/{uid:uuid}/purchased/subscription', response_model=List[PurchasedSubscription_Pydantic])
async def get_client_subscription(uid: uuid.UUID):
    get_qs = models.PurchasedSubscription.filter(client=uid)
    return await PurchasedSubscription_Pydantic.from_queryset(get_qs)


@router.post('/client/{uid:uuid}/purchased/subscription', response_model=PurchasedSubscription_Pydantic)
async def create_client_subscription(uid: uuid.UUID, purchased_sub: PurchasedSubscription_Raw_Pydantic):
    purchased_sub_dct = purchased_sub.dict()
    subscription_quantity_day = await models.Subscription.get(uid=purchased_sub_dct['subscription_id'])
    purchased_sub_dct['uid'] = uuid.uuid4()
    purchased_sub_dct['client_id'] = uid
    purchased_sub_dct['date_endings'] = purchased_sub_dct['date_activation'] + timedelta(subscription_quantity_day.quantity_day)
    get_create_obj = await models.PurchasedSubscription.create(**purchased_sub_dct)
    return await PurchasedSubscription_Pydantic.from_tortoise_orm(get_create_obj)


@router.delete('/client/purchased/subscription/{uid:uuid}')
async def delete_client_subscription(uid: uuid.UUID):
    ps_obj = await models.PurchasedSubscription.get(uid=uid)
    await ps_obj.delete()
    return {"msg": f"Преобретенная подписка удалена"}


@router.get('/client/purchased/subscription/{uid:uuid}', response_model=PurchasedSubscription_Pydantic)
async def get_one_client_subscription(uid: uuid.UUID):
    get_obj = await models.PurchasedSubscription.get(uid=uid)
    return await PurchasedSubscription_Pydantic.from_tortoise_orm(get_obj)


# @router.put('/client/purchased/subscription/{uid:uuid}', response_model=PurchasedSubscription_Pydantic)
# async def update_client_subscription(uid: uuid.UUID, ps: PurchasedSubscription_Raw_Pydantic):
#     get_obj = await models.PurchasedSubscription.get(uid=uid)
#     ps_dct = ps.dict()
#     old_sub = await get_obj.subscription
#     if ps_dct['subscription_id'] != old_sub.uid:
#         ps_dct['date_endings'] = ps_dct['date_activation'] + timedelta(old_sub.quantity_day)
#         ps_dct['date_sale'] = datetime.now()
#     update_obj = get_obj.update_from_dict(ps_dct)
#     await update_obj.save()
#     return await PurchasedSubscription_Raw_Pydantic(update_obj)
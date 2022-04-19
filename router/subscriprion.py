import uuid

from fastapi import APIRouter
from schema import Subscription_Without_Purchased_Pydantic, Subscription_Raw
import models
from typing import List

router = APIRouter(
    tags=['API Subscription']
)


@router.get('/subscription', response_model=List[Subscription_Without_Purchased_Pydantic])
async def get_subscription():
    qs_sub = models.Subscription.all()
    return await Subscription_Without_Purchased_Pydantic.from_queryset(qs_sub)


@router.get('/subscription/{uid:uuid}', response_model=Subscription_Without_Purchased_Pydantic)
async def get_one_subscription(uid: uuid.UUID):
    get_sub = await models.Subscription.get(uid=uid)
    return await Subscription_Without_Purchased_Pydantic.from_tortoise_orm(get_sub)


@router.post('/subscription', response_model=Subscription_Raw)
async def create_subscription(subscription: Subscription_Raw):
    create_sub = await models.Subscription.create(**subscription.dict())
    return await Subscription_Raw.from_tortoise_orm(create_sub)


@router.put('/subscription/{uid:uuid}', response_model=Subscription_Raw)
async def update_subscription(uid: uuid.UUID, subscription: Subscription_Raw):
    get_sub = await models.Subscription.get(uid=uid)
    update_sub = await get_sub.update_from_dict(data=subscription.dict())
    await update_sub.save()
    return await Subscription_Raw.from_tortoise_orm(update_sub)


@router.delete('/subscription/{uid:uuid}')
async def delete_subscription(uid: uuid.UUID):
    get_sub = await models.Subscription.get(uid=uid)
    await get_sub.delete()
    return {'msg': f'Delete subscription {get_sub.name} successful'}
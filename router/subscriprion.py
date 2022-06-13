import uuid

from fastapi import APIRouter
from schema import Subscription_Without_Purchased_Pydantic, Subscription_Raw_Pydantic, PurchasedSubscription_Pydantic
import models
from filter import filter_qs
from typing import List, Optional

router = APIRouter(
    tags=['API Subscription']
)


@router.get('/subscription', response_model=List[Subscription_Without_Purchased_Pydantic])
async def get_subscription(name: Optional[str] = None, gym_lesson: Optional[uuid.UUID] = None,
                           quantity_gym_lesson: Optional[int] = None, quantity_day: Optional[int] = None,
                           price: Optional[int] = None):
    data_subscription = await filter_qs(models.Subscription, Subscription_Without_Purchased_Pydantic, name=name,
                                        gym_lesson=gym_lesson, quantity_gym_lesson=quantity_gym_lesson,
                                        quantity_day=quantity_day, price=price)
    return data_subscription


@router.get('/subscription/purchased', response_model=List[PurchasedSubscription_Pydantic])
async def all_purchased_subscription(subscription: Optional[uuid.UUID] = None, gym_lesson: Optional[uuid.UUID] = None,
                                     client: Optional[uuid.UUID] = None, price: Optional[int] = None,
                                     office: Optional[uuid.UUID] = None):
    data_purchased_subscription = await filter_qs(models.PurchasedSubscription, PurchasedSubscription_Pydantic,
                                                  subscription_id=subscription, gym_lesson_id=gym_lesson,
                                                  client_id=client,
                                                  office_id=office, price=price)
    return data_purchased_subscription


@router.get('/subscription/{uid:uuid}', response_model=Subscription_Without_Purchased_Pydantic)
async def get_one_subscription(uid: uuid.UUID):
    get_sub = await models.Subscription.get(uid=uid)
    return await Subscription_Without_Purchased_Pydantic.from_tortoise_orm(get_sub)


@router.post('/subscription', response_model=Subscription_Raw_Pydantic)
async def create_subscription(subscription: Subscription_Raw_Pydantic):
    subscription = subscription.dict()
    subscription['uid'] = uuid.uuid4()
    create_sub = await models.Subscription.create(**subscription)
    return await Subscription_Raw_Pydantic.from_tortoise_orm(create_sub)


@router.put('/subscription/{uid:uuid}', response_model=Subscription_Raw_Pydantic)
async def update_subscription(uid: uuid.UUID, subscription: Subscription_Raw_Pydantic):
    get_sub = await models.Subscription.get(uid=uid)
    update_sub = await get_sub.update_from_dict(data=subscription.dict())
    await update_sub.save()
    return await Subscription_Raw_Pydantic.from_tortoise_orm(update_sub)


@router.delete('/subscription/{uid:uuid}')
async def delete_subscription(uid: uuid.UUID):
    get_sub = await models.Subscription.get(uid=uid)
    await get_sub.delete()
    return {'msg': f'Delete subscription {get_sub.name} successful'}

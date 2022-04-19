import uuid

from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from tortoise.contrib.pydantic.creator import PydanticMeta
from models import Office, GymRoom, Subscription


class Office_Raw(PydanticMeta):
    exclude = ('gymrooms', 'purchasedsubscriptions', 'uid',)


Office_Pydantic = pydantic_model_creator(Office, name='Office')
Office_Raw_Pydantic = pydantic_model_creator(Office, name='Office_Raw', meta_override=Office_Raw)

GymRoom_Pydantic = pydantic_model_creator(GymRoom, name='GymRoom')


class GymRoom_OfficePK_Pydantic(PydanticModel):
    name: str
    office: uuid.UUID
    description: str


class Subscription_Without_Purchased(PydanticMeta):
    exclude = ('purchasedsubscriptions',)


Subscription_Pydantic = pydantic_model_creator(Subscription, name='Subscription')
Subscription_Without_Purchased_Pydantic = pydantic_model_creator(Subscription, name='Subscription_Without_Purchased',
                                                                 meta_override=Subscription_Without_Purchased)


class Subscription_Raw(PydanticModel):
    gym_lesson: uuid.UUID
    name: str
    quantity_gym_lesson: int
    quantity_day: int
    price: int
    description: str

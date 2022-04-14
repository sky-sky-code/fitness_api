import uuid

from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from tortoise.contrib.pydantic.creator import PydanticMeta
from models import Office, GymRoom


class Office_Raw(PydanticMeta):
    exclude = ('gymrooms', 'purchasedsubscriptions', 'uid',)


Office_Pydantic = pydantic_model_creator(Office, name='Office')
Office_Raw_Pydantic = pydantic_model_creator(Office, name='Office_Raw', meta_override=Office_Raw)

GymRoom_Pydantic = pydantic_model_creator(GymRoom, name='GymRoom')


class GymRoom_OfficePK_Pydantic(PydanticModel):
    name: str
    office: uuid.UUID
    description: str

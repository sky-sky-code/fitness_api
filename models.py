import uuid
from enum import Enum

from tortoise import Tortoise, Model, fields, run_async

import settings
from mixins import User


class Admin(User):
    is_superuser = fields.BooleanField(default=True)


class Trainer(User):
    pass


class Profile(User):
    trainer: fields.OneToOneRelation[Trainer] = fields.OneToOneField('models.Trainer', on_delete=fields.CASCADE)


class Office(Model):
    uid = fields.UUIDField(default=uuid.uuid4(), pk=True)
    name = fields.CharField(max_length=256)
    address = fields.CharField(max_length=2048)
    phone = fields.CharField(max_length=30)
    site = fields.CharField(max_length=512, null=True, blank=True)
    vk_url = fields.CharField(max_length=512, null=True, blank=True)
    facebook_url = fields.CharField(max_length=512, null=True, blank=True)
    instagram_url = fields.CharField(max_length=512, null=True, blank=True)
    description = fields.TextField(null=True, blank=True)


class GymRoom(Model):
    uid = fields.UUIDField(default=uuid.uuid4(), pk=True)
    office: fields.ForeignKeyRelation[Office] = fields.ForeignKeyField('models.Office', on_delete=fields.CASCADE)
    name = fields.CharField(max_length=256)
    description = fields.TextField()


class TypeLesson(str, Enum):
    LESSON_GROUP = 'групповое'
    LESSON_PERSONAL = 'персональное'


class GymLesson(Model):
    uid = fields.UUIDField(default=uuid.uuid4(), pk=True)
    name = fields.CharField(max_length=256)
    type = fields.CharEnumField(TypeLesson, default=TypeLesson.LESSON_GROUP)
    duration = fields.CharField(max_length=256)


class Subscription(Model):
    uid = fields.UUIDField(default=uuid.uuid4(), pk=True)
    gym_lesson: fields.ForeignKeyRelation[GymLesson] = fields.ForeignKeyField('models.GymLesson',
                                                                              on_delete=fields.CASCADE)
    name = fields.CharField(max_length=256)
    quantity_gym_lesson = fields.IntField()
    quantity_day = fields.IntField()
    price = fields.IntField()
    description = fields.TextField()


class PurchasedSubscription(Model):
    uid = fields.UUIDField(default=uuid.uuid4(), pk=True)
    date_sale = fields.DateField(auto_now_add=True)
    subscription: fields.ForeignKeyRelation[Subscription] = fields.ForeignKeyField('models.Subscription',
                                                                                   on_delete=fields.RESTRICT)
    date_activation = fields.DateField()
    date_endings = fields.DateField()
    office: fields.ForeignKeyRelation[Office] = fields.ForeignKeyField('models.Office', on_delete=fields.CASCADE)
    client: fields.ForeignKeyRelation[Profile] = fields.ForeignKeyField('models.Profile')


async def run():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(run())
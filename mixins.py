import uuid

from tortoise import Model, fields


class User(Model):
    uid = fields.UUIDField(default=uuid.uuid4(), pk=True)
    name = fields.CharField(max_length=256)
    surname = fields.CharField(max_length=256)
    pat_name = fields.CharField(max_length=512)
    date_birth = fields.DateField()
    gender = fields.CharField(max_length=1)
    series_passport = fields.CharField(max_length=4, null=True, blank=True)
    number_passport = fields.CharField(max_length=6, null=True, blank=True)
    phone = fields.CharField(max_length=20, null=True, blank=True)
    email = fields.CharField(max_length=512, null=True, blank=True)
    is_staff = fields.BooleanField(default=False)

    class Meta:
        abstract = True

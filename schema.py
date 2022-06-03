from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.pydantic.creator import PydanticMeta
from models import Office, GymRoom, Subscription, GymLesson, Profile, PurchasedSubscription, Service

Office_Pydantic = pydantic_model_creator(Office, name='Office')
Office_Raw_Pydantic = pydantic_model_creator(Office, name='Office_Raw', exclude_readonly=True)

GymRoom_Pydantic = pydantic_model_creator(GymRoom, name='GymRoom')
GymRoom_Raw_Pydantic = pydantic_model_creator(GymRoom, name='GymRoom_Raw', exclude_readonly=True)

GymLesson_Pydantic = pydantic_model_creator(GymLesson, name='GymLesson')
GymLesson_Raw_Pydantic = pydantic_model_creator(GymLesson, name='GymLesson_Raw', exclude_readonly=True)


class Subscription_Without_Purchased(PydanticMeta):
    exclude = ('purchasedsubscriptions',)


Subscription_Pydantic = pydantic_model_creator(Subscription, name='Subscription')
Subscription_Without_Purchased_Pydantic = pydantic_model_creator(Subscription, name='Subscription_Without_Purchased',
                                                                 meta_override=Subscription_Without_Purchased)
Subscription_Raw_Pydantic = pydantic_model_creator(Subscription, name='Subscription_Raw', exclude_readonly=True)

Profile_Pydantic = pydantic_model_creator(Profile, name='Client')
Profile_Raw_Pydantic = pydantic_model_creator(Profile, name='Profile', exclude_readonly=True)

PurchasedSubscription_Pydantic = pydantic_model_creator(PurchasedSubscription, name='PurchasedSubscription')


class PurchasedSubscription_Without_ClientID(PydanticMeta):
    exclude = ('client_id', 'date_sale', 'date_endings',)


PurchasedSubscription_Raw_Pydantic = pydantic_model_creator(PurchasedSubscription,
                                                            name='PurchasedSubscription_Raw',
                                                            exclude_readonly=True,
                                                            meta_override=PurchasedSubscription_Without_ClientID)

Service_Pydantic = pydantic_model_creator(Service, name='Service')
Service_Raw_Pydantic = pydantic_model_creator(Service, name='Service_Raw', exclude_readonly=True)
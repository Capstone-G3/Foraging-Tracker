from django.db.models import (Model, AutoField, CharField, IntegerField, ForeignKey,
                              CASCADE, DateField, EmailField, ImageField)

from foraging_app.models import user


class User_Profile(Model):
    GENDER_CHOICES = [("Male", 2), ("Female", 1), ("Other", 9)]
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=120, null=False)
    last_name = CharField(max_length=120, null=False)
    email = EmailField(max_length=254, null=False)
    home_address = CharField(max_length=254, null=False)
    phone = CharField(max_length=15, default=None)
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=False)
    user_id= ForeignKey('foraging_app.User', on_delete=CASCADE)



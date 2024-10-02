from django.db.models import (Model, AutoField, CharField, IntegerField, ForeignKey,
                              CASCADE, DateField, EmailField, ImageField)

from foraging_app.models import user


class User_Profile(Model):
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=120, null=False)
    last_name = CharField(max_length=120, null=False)
    email = EmailField(max_length=254, null=False)
    home_address = CharField(max_length=254, null=False)
    phone = CharField(max_length=15, default=None)
    gender = [("Male", 2), ("Female", 1), ("Other", 9)]
    user_id= ForeignKey(user.User, on_delete=CASCADE)



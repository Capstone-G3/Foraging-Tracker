from django.db.models import (Model, AutoField, CharField, IntegerField, OneToOneField,
                              CASCADE, DateField, EmailField, ImageField)

from foraging_app.models.user import User


class User_Profile(Model):
    GENDER_CHOICES = [
        (1, "Female"),
        (2, "Male"),
        (9, "Other")
    ]
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=120, null=False)
    last_name = CharField(max_length=120, null=False)
    #got rid of email for ease of using default django libraries
    home_address = CharField(max_length=254, null=False)
    phone = CharField(max_length=15, default=None)
    gender = IntegerField(choices=GENDER_CHOICES, null=False)
    user_id= OneToOneField(User, on_delete=CASCADE) #one user can only have one user profile and vice versa


